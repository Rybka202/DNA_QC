from src.parser.qc_module import Module


class BasicStatistics(Module):

    def __init__(self, infile, outdir):
        super().__init__(infile, outdir)
        self.name = 'Basic Statistics'

    def display_stats(self):
        stats = ''.join(self.lines)
        print(stats)

    def module_output(self):
        super().module_output()
        self.display_stats()
        print('Completed.\n' + '-' * 80)
