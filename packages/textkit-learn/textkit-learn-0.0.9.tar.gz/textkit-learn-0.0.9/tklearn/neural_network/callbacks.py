__all__ = [
    'Callback',
    'CallbackCollection',
]


class Callback:
    def __init__(self):
        self._model = None

    def on_train_batch_start(self, batch, logs=None):
        pass

    def on_train_batch_end(self, batch, logs=None):
        pass

    def on_test_batch_start(self, batch, logs=None):
        pass

    def on_test_batch_end(self, batch, logs=None):
        pass

    def on_predict_batch_start(self, batch, logs=None):
        pass

    def on_predict_batch_end(self, batch, logs=None):
        pass

    def on_epoch_start(self, epoch, logs=None):
        pass

    def on_epoch_end(self, epoch, logs=None):
        pass

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value


class CallbackCollection(Callback):
    def __init__(self, callbacks):
        super(CallbackCollection, self).__init__()
        self.callbacks = callbacks

    def __getattribute__(self, item):
        if item in [
            'on_train_batch_start', 'on_train_batch_end', 'on_test_batch_start', 'on_test_batch_end',
            'on_predict_batch_start', 'on_predict_batch_end', 'on_epoch_start', 'on_epoch_end',
        ]:
            def apply_callback(*args, **kwargs):
                for c in self.callbacks:
                    if hasattr(c, item):
                        getattr(c, item)(*args, **kwargs)

            return apply_callback
        else:
            return super(CallbackCollection, self).__getattribute__(item)


class LoggerCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        print('Epoch: {}'.format(epoch))
