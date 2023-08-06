import pandas as pd

from reutils import logging_v2 as logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

logging.basicConfig(format=logging.LOGGING_FORMAT)

__all__ = [
    'Dataset',
    'TextDataset',
]


class Dataset:
    """Dataset: Key-Value store for loading datasets. Less restricted than `pd.DataFrames` more restricted than `dict`.
    Stores values as provided np.array/pd.DataFrame/pd.Series/List(as pd.Series).

    The main constraint is that the value must have the same number of rows.
    """

    def __init__(self, data=None):
        self._data = {}
        self._attributes = []
        self._length = None
        self._from_dict(data=data)

    def __len__(self):
        return self._length

    def __getitem__(self, idx):
        return [self._data[a][idx] for a in self._attributes]

    def __iter__(self):
        records = [self._data[a] for a in self._attributes]
        for record in zip(*records):
            yield record

    def __getstate__(self):
        return vars(self)

    def __setstate__(self, state):
        vars(self).update(state)

    def __getattr__(self, item):
        if item in self._data:
            return self._data[item]
        raise AttributeError

    def assign(self, **kwargs):
        copy = Dataset()
        copy._data = self._data
        copy._attributes = self._attributes
        copy._length = self._length
        for k, v in kwargs.items():
            copy._data[k] = self._format_value(k, v)
        return copy

    def _format_value(self, k, v):
        if self._length is None:
            self._length = len(v)
        if len(v) != self._length:
            _args = (k, self._length, len(v))
            raise ValueError('invalid number of rows for column \'{}\'; expected {}, found {} rows.'.format(*_args))
        if not hasattr(v, 'shape'):
            return pd.Series(v)
        else:
            return v

    @classmethod
    def from_dict(cls, data=None):
        return cls()._from_dict(data=data)

    def _from_dict(self, data=None):
        if data is None:
            data = []
        orient = 'records'
        if isinstance(data, dict):
            orient = 'columns'
        if orient == 'records':
            for record in data:
                self._attributes += record.keys()
            for record in data:
                self._length += 1
                for attribute in self._attributes:
                    if attribute not in self._data:
                        self._data[attribute] = []
                    value = record[attribute]
                    self._data[attribute].append(value)
            for k, v in self._data.items():
                self._data[k] = self._format_value(k, v)
        elif orient == 'columns':
            self._attributes += data.keys()
            for k, v in data.items():
                self._data[k] = self._format_value(k, v)
        return self


class TextDataset(Dataset):
    def __init__(self, records):
        super().__init__(records)
        if 'text' not in self._attributes:
            raise AttributeError('\'TextDataset\' object has no attribute \'text\'')
