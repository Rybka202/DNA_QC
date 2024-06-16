import subprocess
import os
import zipfile
import time
import shutil

from fastapi import FastAPI
from boto3 import client
from sqlalchemy import text
from fpdf import FPDF

from src import brokerConnection
from parser import adapter_content, base_n_content, base_seq_content, base_seq_qlty, basic_stats,\
    overrepresented_seqs, seq_duplication_levels, seq_gc_content, seq_len_distribution, \
    seq_qlty_scores, tile_seq_qlty
from src.database import conn
from src.config import S3_HOST, S3_PORT, S3_NAME, S3_PASS


app = FastAPI(
    title="Executors"
)

s3 = client('s3',
            endpoint_url=f'http://{S3_HOST}:{S3_PORT}',
            aws_access_key_id=S3_NAME,
            aws_secret_access_key=S3_PASS)

def analyze(input_file: str):
    command = "java -Xmx6144M -classpath .;./sam-1.103.jar;./jbzip2-0.9.jar uk.ac.babraham.FastQC.FastQCApplication " + "..\\" + input_file
    try:
        print(os.getcwd())
        os.chdir("../FastQC/")
        print(os.getcwd())
        subprocess.run(command.split())
        print(os.getcwd())
        os.chdir("../../")
        print(os.getcwd())
    except subprocess.CalledProcessError as e:
        raise e


def process(input_path):
    outdir = "outdir/"
    module_options = dict(
        per_base_seq_qlty=base_seq_qlty.PerBaseSeqQlty,
        per_tile_seq_qlty=tile_seq_qlty.PerTileSeqQlty,
        per_seq_qlty_scores=seq_qlty_scores.PerSeqQltyScores,
        per_base_seq_content=base_seq_content.PerBaseSeqContent,
        per_sequence_gc_content=seq_gc_content.PerSeqGCContent,
        per_base_n_content=base_n_content.PerBaseNContent,
        seq_len_dist=seq_len_distribution.SeqLengthDistribution,
        seq_dup_levels=seq_duplication_levels.SeqDuplicationLevels,
        overrep_seq=overrepresented_seqs.OverrepresentedSeqs,
        adapter_content=adapter_content.AdapterContent
    )

    try:
        stats = basic_stats.BasicStatistics(input_path, outdir)
        stats.module_output()
    except FileNotFoundError:
        raise 'Input file not found.'
    for name in module_options:
        module = module_options[name](input_path, outdir)
        module.module_output()


def generate_pdf(name):
    pdf = FPDF()
    pdf.add_font("Sans", style="", fname="NotoSans-Regular.ttf")
    pdf.add_font("Sans", style="B", fname="NotoSans-Bold.ttf")
    for path in os.listdir("outdir"):
        if path == 'Overrepresented_sequences':
            pdf.add_page()
            pdf.set_font("Sans", size=20)
            with open(f"outdir/{path}/filter.txt") as f:
                res = f.readline()
            res = res.strip().lower()
            if res == "pass":
                res = "успешно пройден"
            elif res == "warn":
                res = "пройден с незначительными отклонениями"
            else:
                res = "не пройден"
            pdf.multi_cell(w=190, h=15, text=f"Наиболее встречаемые последовательности: {res}")
            pdf.ln(h=5)
            with open(f"outdir/{path}/QC_report.txt") as f:
                text = f.readlines()
                columns = text[1][1:]
                col = columns.split()
                data = text[2:]
                for i in range(len(data)):
                    data[i] = data[i].split(maxsplit=len(col) - 2)
            data.insert(0, col)
            pdf.set_font("Sans", size=10)
            tbody = ''
            for i in range(1, len(data)):
                td = f"<tr><td>{'</td><td>'.join(data[i])}</td> </tr>\n"
                tbody += td
            pdf.write_html(
                f"""<table border="1"><thead><tr>
                    <th width="25%">Последовательности</th>
                    <th width="25%">Количество</th>
                    <th width="15%">Процент содержания</th>
                    <th width="35%">Название</th>
                </tr></thead><tbody>{tbody}</tbody></table>""",
                table_line_separators=True)
            continue
        pdf.add_page()
        pdf.set_font("Sans", size=20)
        with open(f"outdir/{path}/filter.txt") as f:
            res = f.readline()
        res = res.strip().lower()
        if res == "pass":
            res = "успешно пройден"
        elif res == "warn":
            res = "пройден с незначительными отклонениями"
        else:
            res = "не пройден"
        path_dict = {
            "Adapter_Content": "Адаптерное содержание",
            "Per_base_N_content": "Содержание N в основаниях",
            "Per_base_sequence_content": "Содержание базовой последовательности",
            "Per_base_sequence_quality": "Качество базовой последовательности",
            "Per_sequence_GC_content": "Содержание ГЦ в последовательности ридов",
            "Per_sequence_quality_scores": "Оценка качества последовательностей ридов",
            "Per_tile_sequence_quality": "Качество потоковой ячейки в последовательности",
            "Sequence_Duplication_Levels": "Повторяющиеся последовательности",
            "Sequence_Length_Distribution": "Распределение длины последовательности"
        }
        pdf.multi_cell(w=190, h=15, text=f"{path_dict[path]}: {res}")
        pdf.ln(h=5)
        pdf.image(f"outdir/{path}/graph.jpg", w=pdf.epw)
    pdf.output(name)

@app.get("/startup")
def startup():
    while True:
        brokerConnection.get_message()
        msg = brokerConnection.get_msg()
        if msg != "":
            try:
                s3.download_file(Bucket='input', Key=msg, Filename=msg)
                analyze(msg)
                s3.delete_object(Bucket='input', Key=msg)
                name = f'{msg[:msg.index(".")]}_fastqc'
                with zipfile.ZipFile(f'{name}.zip', 'r') as zf:
                    zf.extract(f'{name}/fastqc_data.txt')
                os.remove(msg)
                os.remove(f'{name}.zip')
                os.remove(f'{name}.html')
                process(f'{name}/fastqc_data.txt')
                shutil.rmtree(name)
                doc = f'{msg[:msg.index(".")]}.pdf'
                generate_pdf(doc)
                shutil.rmtree('outdir')
                s3.put_object(Bucket='output', Key=doc, Body=open(doc, 'rb'))
                stmt = f"UPDATE file SET stage=2 WHERE id='{msg}'"
                conn.execute(text(stmt))
                conn.commit()
                os.remove(doc)
                brokerConnection.clear_msg()
            except subprocess.CalledProcessError as e:
                s3.delete_object(Bucket='input', Key=msg)
                os.remove(msg)
                stmt = f"UPDATE file SET stage=3 WHERE id='{msg}'"
                conn.execute(text(stmt))
                conn.commit()

        else:
            time.sleep(0.5)