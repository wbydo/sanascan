import os

def _readline(self, dir_):
    path_ = os.path.join(dir_ + self.corpus_file_id)
    with open(path_) as f:
        for line in iter(f.readline, ''):
            yield line.strip()
