import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.parser.qc_module import Module


class AdapterContent(Module):

    def __init__(self, fastqc, outdir):
        super().__init__(fastqc, outdir)
        self.name = 'Adapter Content'

    def prep_data(self):
        try:
            lines, columns = self.clean_lines()
            data = [(line[0], float(line[1]), float(line[2]), float(line[3]),
                     float(line[4]), float(line[5]), float(line[6])) for line in lines[2:]]
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            df = pd.DataFrame(data=data, columns=columns)
            df.index = df['Position']
        return df

    def create_graph(self):
        df = self.prep_data()
        # plot graph
        sns.set_style('darkgrid')
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x=df['Position'],
                     y=df['Illumina Universal Adapter'],
                     label='Illumina Universal Adapter', color='red')

        sns.lineplot(x=df['Position'],
                     y=df["Illumina Small RNA 3' Adapter"],
                     label="Illumina Small RNA 3' Adapter", color='blue')

        sns.lineplot(x=df['Position'],
                     y=df["Illumina Small RNA 5' Adapter"],
                     label="Illumina Small RNA 5' Adapter", color='green')

        sns.lineplot(x=df['Position'],
                     y=df['Nextera Transposase Sequence'].cumsum(),
                     label='Nextera Transposase Sequence', color='yellow')
        sns.lineplot(x=df['Position'], y=df['PolyA'],
                     label='PolyA', color='purple')

        sns.lineplot(x=df['Position'], y=df['PolyG'],
                     label='PolyG', color='orange')

        ax.legend(loc='best', facecolor='white')
        ax.set_xlabel('Позиция в риде (осн)')
        ax.set_ylabel('Камулятивные пропорции данных (%)')
        plt.yticks(np.arange(0, 6, 0.5))
        ax.axes.set_xlim(0)
        tick_labels = np.concatenate([df['Position'][0:9:2].values,
                                      df['Position'][10:50:4].values,
                                      df['Position'][50::10].values])
        plt.xticks(tick_labels, fontsize=8)
        plt.yticks(fontsize=8)
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
        for s in ['left', 'bottom']:
            ax.spines[s].set_linewidth(1)
            ax.spines[s].set_color('black')
        # remove top axis
        ax.spines['top'].set_visible(False)
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
