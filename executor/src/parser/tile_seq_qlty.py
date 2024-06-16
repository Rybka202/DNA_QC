"""This module contains functionality for generating reports and visualising
Per tile sequence quality data from FastQC files.
"""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.parser.qc_module import Module


class PerTileSeqQlty(Module):

    def __init__(self, infile, outdir):
        super().__init__(infile, outdir)
        self.name = 'Per tile sequence quality'

    def prep_data(self):
        try:
            lines, columns = self.clean_lines()
            # cast data in each line to appropriate type
            data = ((int(line[0]), line[1], float(line[2])) for line in lines[2:])
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            # exclude module header and column lines
            df = pd.DataFrame(data, columns=columns)
            # create pivot table
            df = df.pivot(index='Tile', columns='Base', values='Mean')
            df = df.sort_values(by='Tile', ascending=False)
            return df

    def create_graph(self):
        df = self.prep_data()
        # set up figure
        fig, ax = plt.subplots(figsize=(12, 6))
        # generate custom diverging palette
        sns.heatmap(df, cmap='RdBu', cbar=False)
        ax.set_xlabel('Позиция в риде (осн)', fontsize=8)
        ax.set_ylabel('Потоковая ячейка', fontsize=8)
        plt.xticks(np.arange(df.columns.size), df.columns, rotation=0,
                   fontsize=6, ha='left')
        ax.set_yticklabels(df.index[::4], fontsize=6)
        ax.yaxis.set_ticks_position('none')
        ax.xaxis.set_ticks_position('none')

        # save figure as png
        path = os.path.join(self.dir_name, 'graph.jpg')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'Graph file generated for {self.name}.')

    def module_output(self):
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
