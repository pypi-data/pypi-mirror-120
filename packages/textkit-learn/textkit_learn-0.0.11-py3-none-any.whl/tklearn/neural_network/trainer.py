import abc
import copy

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from six import string_types
from sklearn.utils.multiclass import type_of_target
from torch.utils.data.dataloader import DataLoader, default_collate

from tklearn.neural_network.callbacks import CallbackCollection
from tklearn.utils import progress

__all__ = [
    'TorchTrainer'
]


def _get_item(v, idx):
    if isinstance(v, (pd.Series, pd.DataFrame)):
        return v.iloc[idx]
    else:
        return v[idx]


class TrainerDataset(torch.utils.data.Dataset):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getitem__(self, item):
        return {k: _get_item(v, item) for k, v in self.kwargs.items()}

    def __len__(self):
        return len(next(iter(self.kwargs.values())))


def custom_collate(batch):
    if len(batch) < 1:
        return default_collate(batch)
    repr_elem = batch[0]
    # if batch is a list of strings
    if isinstance(repr_elem, list) and (len(repr_elem) > 0) and isinstance(repr_elem[0], string_types):
        return batch
    elif isinstance(repr_elem, dict):
        return {k: custom_collate([item[k] for item in batch]) for k in repr_elem.keys()}
    return default_collate(batch)


class TorchTrainer(abc.ABC):
    def __init__(self, callbacks=None, device=None):
        super(TorchTrainer, self).__init__()
        if callbacks is None:
            callbacks = []
        self.callbacks = callbacks
        self.device = device
        self._model_ = None
        self._history_ = None
        self._type_of_target_ = None

    def _train(self, X, y=None, epochs=1, batch_size=32, shuffle=True, verbose=1):
        self.type_of_target = type_of_target(y)
        dataset = TrainerDataset(X=X, y=y)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, collate_fn=custom_collate)
        self.model = self.build_model()
        criterion = self.criterion
        optimizer = self.optimizer
        callbacks = self._get_callbacks()
        self.history = []
        for epoch in range(epochs):  # loop over the dataset multiple times
            callbacks.on_epoch_start(epoch, self.history)
            running_loss = 0.0
            batch_history = []
            progress_bar = progress() if verbose > 0 else None
            for i, data in (enumerate if progress_bar is None else progress_bar.enumerate)(dataloader, 0):
                callbacks.on_train_batch_start(i)
                batch_X, batch_y = data['X'], data['y']
                # zero the parameter gradients
                optimizer.zero_grad()
                # forward + backward + optimize
                outputs = self.model(batch_X)
                batch_y = batch_y.type_as(outputs)
                _loss = criterion(outputs, batch_y)
                _loss.backward()
                optimizer.step()
                # print statistics
                running_loss += _loss.item()
                batch_log = {
                    'epoch': epoch + 1,
                    'batch': i + 1,
                    'loss': running_loss / (i + 1),
                }
                if progress_bar is not None:
                    progress_bar.set_description(
                        'Epoch: {epoch:3d}/{epochs:<3d}\tBatch: {batch:4d}/{batch_size:<4d}\tLoss:{loss:0.4f}'.format(
                            batch_size=batch_size, epochs=epochs, **batch_log
                        )
                    )
                batch_history.append(batch_log)
                callbacks.on_train_batch_end(i, batch_log)
            callbacks.on_epoch_end(epoch, batch_history)
            self.history += batch_history
        return self

    def get_device(self):
        if (self.device is None) and (torch.cuda.is_available()):
            return 'cuda'
        elif self.device is None:
            return 'cpu'
        else:
            return self.device

    @property
    def criterion(self):
        loss = None
        if self.type_of_target in ['multiclass', 'multiclass-multioutput']:
            loss = nn.CrossEntropyLoss()
        elif self.type_of_target in ['multilabel-indicator', 'binary']:
            loss = nn.BCEWithLogitsLoss()
        if loss is None:
            raise AttributeError('Loss is not defined.')
        return loss

    @property
    def optimizer(self):
        return optim.SGD(self._model_.parameters(), lr=0.001, momentum=0.9)

    def build_model(self):
        raise NotImplementedError

    @property
    def model(self):
        if self._model_ is None:
            raise AttributeError('Model (\'model\') is not available yet.')
        return self._model_

    @model.setter
    def model(self, value):
        self._model_ = value

    @property
    def type_of_target(self):
        if self._type_of_target_ is None:
            raise AttributeError('Type of target attribute (\'type_of_target\') is not available yet.')
        return self._type_of_target_

    @type_of_target.setter
    def type_of_target(self, value):
        self._type_of_target_ = value

    @property
    def history(self):
        return self._history_

    @history.setter
    def history(self, value):
        self._history_ = value

    def _get_callbacks(self):
        callbacks = []
        for x in self.callbacks:
            x = copy.copy(x)
            x.model = self
            callbacks.append(x)
        callbacks = CallbackCollection(callbacks)
        callbacks.model = self
        return callbacks
