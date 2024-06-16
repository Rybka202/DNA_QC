import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.parser.qc_module import Module


class PerBaseNContent(Module):

    def __init__(self, fastqc, outdir):
        super().__init__(fastqc, outdir)
        self.name = 'Per base N content'

    def prep_data(self):
        try:
            lines, columns = self.clean_lines()
            data = [(str(line[0]), float(line[1])) for line in lines[2:]]
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
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.lineplot(x=df['Base'], y=df['N-Count']*100, label='%N',
                     color='red')
        ax.legend(facecolor='white')
        plt.xlim(df.index.min(), df.index.max())
        tick_labels = np.concatenate([df.index[0:9:2],
                                      df.index[10:50:4],
                                      df.index[50::10]])
        plt.xticks(tick_labels)
        plt.yticks(np.arange(0, 101, 10))
        plt.ylim(0, 100)
        ax.set_xlabel('Позиция в риде (осн)')
        ax.set_ylabel('Процент вызова основания(%)')
        # Show the spine of the axes
        for s in ['left', 'bottom']:
            ax.spines[s].set_linewidth(1)
            ax.spines[s].set_color('black')
        # remove top axis
        ax.spines['top'].set_visible(False)
        # save figure
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
