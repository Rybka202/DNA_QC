import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.parser.qc_module import Module


class PerBaseSeqContent(Module):

    def __init__(self, fastqc, outdir):
        super().__init__(fastqc, outdir)
        self.name = 'Per base sequence content'

    def prep_data(self):
        try:
            lines, columns = self.clean_lines()
            data = [(str(line[0]), float(line[1]), float(line[2]), float(line[3]),
                     float(line[4])) for line in lines[2:]]
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            df = pd.DataFrame(data=data, columns=columns)
            df.index = df['Base']
            return df

    def create_graph(self):
        df = self.prep_data()
        sns.set_style('darkgrid')
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x=df['Base'], y=df['G'], color='red', label='% Г')
        sns.lineplot(x=df['Base'], y=df['A'], color='blue', label='% А')
        sns.lineplot(x=df['Base'], y=df['T'], color='green', label='% Т')
        sns.lineplot(x=df['Base'], y=df['C'], color='black', label='% Ц')

        # configure legend
        ax.legend(loc='upper right', facecolor='white', frameon=True)
        # configure axes
        ax.set_xlabel('Позиция в риде (осн)')
        ax.set_ylabel('Пропорция (%)')
        tick_labels = np.concatenate([df.index[0:9:2],
                                      df.index[10:50:4],
                                      df.index[50::10]])
        plt.xticks(tick_labels)
        ax.axes.set_xlim(0)
        ax.set_yticks(np.arange(0, 101, 10))

        # configure spines of axes
        for s in ['left', 'bottom']:
            ax.spines[s].set_linewidth(1)
            ax.spines[s].set_color('black')
        ax.spines['top'].set_visible(False)

        # Save plot
        path = os.path.join(self.dir_name, 'graph.jpg')
        plt.savefig(path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f'Graph file generated for {self.name}.')

    def module_output(self):
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
