import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.parser.qc_module import Module


class PerSeqQltyScores(Module):

    def __init__(self, fastqc, outdir):
        super().__init__(fastqc, outdir)
        self.name = 'Per sequence quality scores'

    def prep_data(self):
        try:
            lines, columns = self.clean_lines()
            data = [(int(line[0]), float(line[1])) for line in lines[2:]]
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            df = pd.DataFrame(data=data, columns=columns)
            df.index = df['Quality']
            return df

    def create_graph(self):
        df = self.prep_data()
        # plot graph
        sns.set_style('darkgrid')
        fig, ax = plt.subplots(1, 1)
        sns.lineplot(x=df['Quality'], y=df['Count'], color='red')
        ax.set_xlabel('Качественная оценка рида')
        ax.set_ylabel('Количество')
        ax.axes.set_ylim(0)
        plt.xticks(df.index, fontsize=8)
        # turn off scientific notation on y-axis
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
        plt.yticks(ax.get_yticks(), fontsize=8)
        # get coordinates for most frequent quality
        max_x, max_y = df.loc[df['Count'] == df['Count'].max()].iloc[0, :]
        # annotate maximum point to indicated average quality per read
        bbox_props = dict(boxstyle='round', fc='w', ec='0.5', alpha=0.9)
        ax.text(max_x, max_y, 'Средняя оценка в риде', ha='center',
                va='center', size=12, bbox=bbox_props, color='red')

        # show spines of axes
        for s in ['left', 'bottom']:
            ax.spines[s].set_linewidth(1)
            ax.spines[s].set_color('black')
        # Don't show top axis to prevent overlap
        ax.spines['top'].set_visible(False)

        # save plot as PNG file
        path = os.path.join(self.dir_name, 'graph.jpg')
        plt.savefig(path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f'Graph file generated for {self.name}.')

    def module_output(self):
        """Generate output for Per sequence quality scores analysis.

        :return: None
        :rtype: None
        """
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
