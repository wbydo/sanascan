class BaseCorpusFile:
    def _readline(self, file_path):
        with open(file_path) as f:
            for line in iter(f.readline, ''):
                yield line.strip()
