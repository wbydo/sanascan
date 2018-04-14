class PostsExtractor:
    def apply(self, strategy, path):
        with open(path) as f:
            for line in iter(f.readline, ''):
                yield strategy.extract_post(line)
