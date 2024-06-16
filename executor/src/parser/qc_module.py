import os
import sys
from abc import ABC, abstractmethod


class Module(ABC):

    def __init__(self, infile, outdir):
        self.lines = []
        self.name = ''
        self.dir_name = ''  # basic stats doesn't have this
        self.infile = infile
        self.outdir = outdir

    def parse_text(self):
        with open(self.infile, 'r') as f:
            for line in f:
                if line.startswith(f'>>{self.name}'):
                    self.lines.append(line)
                    for modline in f:
                        if not modline.startswith('>>END'):
                            self.lines.append(modline)
                        else:
                            break
        # check the module is in the file
        try:
            # if module is absent from file the lines attribute will be empty
            if not len(self.lines):
                raise ValueError
        except ValueError:
            print(f'Module "{self.name}" missing from input file.')
            sys.exit(1)

    def make_dir(self):
        dir_name = self.name.replace(' ', '_')
        self.dir_name = os.path.join(self.outdir, dir_name)
        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)
        else:
            while True:
                answer = input(
                    f'WARNING: {self.name} module directory exists in output '
                    f'directory, any report files in the directory will be '
                    f'overwritten. Proceed (Y/N)? ')
                if answer.lower() == 'y':
                    break
                elif answer.lower() == 'n':
                    sys.exit()

    def create_report(self):
        path = os.path.join(self.dir_name, 'QC_report.txt')
        with open(path, 'w') as f:
            lines = ''.join(self.lines)
            f.write(lines)
            print(f'Report text file generated for {self.name}.')

    def create_filter_text(self):
        path = os.path.join(self.dir_name, 'filter.txt')
        filter_info = self.lines[0].split('\t')[1]
        with open(path, 'w') as f:
            f.write(filter_info)
            print(f'Filter text file generated for {self.name}.')

    def clean_lines(self):
        lines = [line.strip('\n').split('\t') for line in self.lines]
        columns = [colname.strip('#') if colname.startswith('#') else colname
                   for colname in lines[1]]
        return lines, columns

    @abstractmethod
    def module_output(self):
        self.parse_text()
        print(f'Generating output for {self.name}...')
