import torch
from torch import nn
from tklearn.embedding import WordEmbedding
from tklearn.neural_network import layers
from tklearn.neural_network.trainer import TorchTrainer

__all__ = [
    'Kim2014ConvModel',
]


# noinspection PyAbstractClass,PyMethodMayBeStatic
class Kim2014ConvNet(nn.Module):
    def __init__(self, variant='CNN-multichannel', embeddings: WordEmbedding = None, embedding_dim=300,
                 vocabulary=None, output_size=1):
        """
        Parameters
        ----------
        variant - Variant from paper to load
            CNN-rand : Baseline model where all words are randomly initialized and then modified
                during training (aka CNN-non-static-rand).
            *-rand : Initialize word embeddings randomly with selected model.
            CNN-static : Initialize pre-trained vectors from provided word2vec.
                All words—including the unknown ones that are randomly initialized—are kept static
                and only the other parameters of the model are learned.
            CNN-non-static : Same as CNN-static but the pre-trained vectors are fine-tuned for each task
            CNN-multichannel : Two sets of word vectors. Each set of vectors is treated as a \'channel\' and
                each filter is applied to both channels, but gradients are back-propagated
                only through one of the channels. Hence the model is able to fine-tune one set
                of vectors while keeping the other static. Both channels are initialized with word2vec.
        embeddings - embeddings
        embedding_dim - dimension of embeddings if embeddings is None
        vocabulary - vocabulary
        """
        super(Kim2014ConvNet, self).__init__()
        if (vocabulary is None) and ('<pad>' not in vocabulary):
            vocabulary = {'<pad>': 0}
        if embeddings is not None:
            embedding_dim = embeddings.shape[1]
        self.variant = variant
        self.embeddings = embeddings
        self.embedding_dim = embedding_dim
        self.vocabulary = vocabulary
        # init model parameters
        self.vocab_size = len(self.vocabulary)
        in_channels = 1
        if self.variant.startswith('CNN-static'):
            self.embeddings_layer = None
            self.embeddings_layer_static = nn.Embedding(self.vocab_size, self.embedding_dim)
            self.embeddings_layer_static.weight.requires_grad = False
        elif self.variant.startswith('CNN-multichannel'):
            self.embeddings_layer = nn.Embedding(self.vocab_size, self.embedding_dim)
            self.embeddings_layer_static = nn.Embedding(self.vocab_size, self.embedding_dim)
            self.embeddings_layer_static.weight.requires_grad = False
            in_channels = 2
        else:
            self.embeddings_layer = nn.Embedding(self.vocab_size, self.embedding_dim)
            self.embeddings_layer_static = None
        if 'rand' not in self.variant:
            if self.embeddings is None:
                raise AttributeError('Word embedding not provided for variant \'{variant}\'. '
                                     'Change variant to \'CNN-rand\' or provide embeddings.'.format(variant=variant))
            embedding_matrix = self.embeddings.embedding_matrix(self.vocabulary)
            if self.embeddings_layer is not None:
                self.embeddings_layer.weight = nn.Parameter(torch.tensor(embedding_matrix, dtype=torch.float32))
            if self.embeddings_layer_static is not None:
                self.embeddings_layer_static.weight = nn.Parameter(torch.tensor(embedding_matrix, dtype=torch.float32))
        out_channels = 100
        kernel_sizes = [(i, self.embedding_dim) for i in [2, 3, 4]]
        stride = 1
        padding = 0
        output_input_size = 0
        self.conv_pool_layers = nn.ModuleList()
        for kernel_size in kernel_sizes:
            conv_layer = nn.Conv2d(in_channels, out_channels * in_channels, kernel_size, stride=stride,
                                   padding=padding, groups=in_channels)
            flatten_layer = layers.Flatten(start_dim=2, end_dim=-1)
            pool_layer = layers.GlobalMaxPooling()
            self.conv_pool_layers.append(nn.Sequential(conv_layer, flatten_layer, pool_layer))
            output_input_size += (out_channels * in_channels)
        self.output = nn.Linear(output_input_size, output_size)

    def forward(self, inputs, **kwargs):
        token_sequence = [[self.vocabulary[w] for w in sent] for sent in inputs]
        context_indexes = torch.tensor(token_sequence, dtype=torch.long)
        embeds = []
        if self.embeddings_layer is not None:
            out = self.embeddings_layer(context_indexes)
            out = torch.unsqueeze(out, 1)
            embeds.append(out)
        if self.embeddings_layer_static is not None:
            out = self.embeddings_layer_static(context_indexes)
            out = torch.unsqueeze(out, 1)
            embeds.append(out)
        embed = torch.cat(embeds, dim=1)
        conv_out = []
        for conv_pool_layer in self.conv_pool_layers:
            out = conv_pool_layer(embed)
            conv_out.append(out)
        conv_out = torch.cat(conv_out, dim=1)
        return self.output(conv_out)


class Kim2014ConvModel(TorchTrainer):
    def __init__(self, variant='CNN-multichannel', embeddings: WordEmbedding = None, embedding_dim=300,
                 vocabulary=None, epochs=1, batch_size=50):
        super(Kim2014ConvModel, self).__init__()
        self.variant = variant
        self.embeddings = embeddings
        self.embedding_dim = embedding_dim
        self.vocabulary = vocabulary
        self.epochs = epochs
        self.batch_size = batch_size
        # available after fit
        self.output_size_ = None

    def fit(self, X, y=None):
        self.output_size_ = y.shape[1]
        self._train(X, y, epochs=self.epochs, batch_size=self.batch_size)
        return self

    def build_model(self):
        return Kim2014ConvNet(
            variant=self.variant, embeddings=self.embeddings, embedding_dim=self.embedding_dim,
            vocabulary=self.vocabulary, output_size=self.output_size_
        )
