import os

def _readline(self, dir_):
    path_ = os.path.join(dir_ + self.name)
    with open(path_) as f:
        for line in iter(f.readline, ''):
            yield line.strip()