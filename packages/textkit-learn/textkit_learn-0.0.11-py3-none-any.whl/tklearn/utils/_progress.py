from tklearn.config import config

__all__ = [
    'progress',
]

DEFAULT_ENGINE = config['DEFAULT'].get('progress.engine', 'tqdm')

_enumerate = enumerate
_range = range


class ProgressIterator:
    def __init__(self, engine=DEFAULT_ENGINE):
        self._engine = engine
        self.p = None

    def __call__(self, *args, **kwargs):
        with self.engine(*args, **kwargs) as p:
            self.p = p
            for x in p:
                yield x

    def range(self, *args, **kwargs):
        with self.engine(_range(*args, **kwargs)) as p:
            self.p = p
            for x in p:
                yield x

    def enumerate(self, *args, **kwargs):
        iter = list(_enumerate(*args, **kwargs))
        with self.engine(iter) as p:
            self.p = p
            for i, x in p:
                yield i, x

    def set_description(self, *args, **kwargs):
        if self._engine == 'tqdm':
            self.p.set_description(*args, **kwargs)
        else:
            return

    def engine(self, *args, **kwargs):
        if self._engine == 'tqdm':
            from tqdm import tqdm
            return tqdm(*args, **kwargs)
        else:
            raise ValueError('Invalid value for progress module, found {} expected one of [\'tqdm\'].')


class ProgressBuilder:
    def __call__(self, *args, **kwargs):
        return ProgressIterator(*args, **kwargs)

    def __getattr__(self, item):
        return getattr(ProgressIterator(), item)


progress = ProgressBuilder()
