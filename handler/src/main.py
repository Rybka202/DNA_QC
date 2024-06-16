from uuid import uuid1
from datetime import datetime

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from boto3 import client
from botocore.exceptions import ClientError
from sqlalchemy import insert, select, join, desc, delete

from brokerConnection import send_message
from models import file as fileTable
from models import stage
from database import conn
from config import S3_HOST, S3_PORT, S3_NAME, S3_PASS


app = FastAPI(
    title="Handler"
)

s3 = client('s3',
            endpoint_url=f'http://{S3_HOST}:{S3_PORT}',
            aws_access_key_id=S3_NAME,
            aws_secret_access_key=S3_PASS)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def check_bucket_exists(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucket":
            return False
        else:
            raise
    return True

@app.on_event("startup")
def start():
    if not check_bucket_exists('input'):
        s3.create_bucket(Bucket='input')
    if not check_bucket_exists('output'):
        s3.create_bucket(Bucket='output')
    return

@app.post("/download")
async def download(file: UploadFile = File(...)):
    id = str(uuid1())
    filename_id = id + file.filename[file.filename.rindex('.', 0, -3):]
    stmt = insert(fileTable).values([filename_id, file.filename, f'{id}.pdf', datetime.now(), 1])
    conn.execute(stmt)
    conn.commit()
    s3.put_object(Bucket='input', Key=filename_id, Body=file.file)
    msg = filename_id
    await send_message(msg)
    return {"id": filename_id}

@app.get("/analyzes")
async def get_analyzes():
    j = join(fileTable, stage, fileTable.c.stage == stage.c.id)
    query = select(fileTable.c.id, fileTable.c.fileName,
                   fileTable.c.time, stage.c.stepOfDevelopment).order_by(desc(fileTable.c.time)).select_from(j)
    result = conn.execute(query)
    res = {"status": "ok", "data": []}
    data = result.all()
    for i in range(len(data)):
        res["data"].append({
            "id": data[i][0],
            "fileName": data[i][1],
            "time": data[i][2].strftime("%H:%M %d.%m.%Y"),
            "stage": data[i][3],
        })
    return JSONResponse(content=jsonable_encoder(res))

@app.delete("/delete/{id}")
def delete_file(id: str):
    query = select(fileTable.c.stage).where(fileTable.c.id == id)
    res = conn.execute(query)
    if res.scalars().all()[0] == 2:
        query = select(fileTable.c.analyze_id).where(fileTable.c.id == id)
        result = conn.execute(query)
        s3.delete_object(Bucket='output', Key=result.scalars().all()[0])
        del_query = delete(fileTable).where(fileTable.c.id == id)
        conn.execute(del_query)
        conn.commit()
    elif res.scalars().all()[0] == 3:
        del_query = delete(fileTable).where(fileTable.c.id == id)
        conn.execute(del_query)
        conn.commit()
    return {"status": "ok"}

@app.get("/upload/{id}")
async def upload(id: str):
    query = select(fileTable).where(fileTable.c.id==id)
    result = conn.execute(query)
    res = []
    for row in result:
        res = list(row).copy()
    if res != [] and res[-1] != 1:
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': 'output',
                                                'Key': res[2]},
                                        ExpiresIn=60)
        return JSONResponse(content=jsonable_encoder({"data": url}))

    return {"data": ""}