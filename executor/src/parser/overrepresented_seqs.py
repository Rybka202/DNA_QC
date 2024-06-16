from src.parser.qc_module import Module


class OverrepresentedSeqs(Module):

    def __init__(self, fastqc, outdir):
        super().__init__(fastqc, outdir)
        self.name = 'Overrepresented sequences'

    def module_output(self):
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        print('Completed.\n' + '-' * 80)
