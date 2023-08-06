import torch
from torch import nn
import torch.nn.functional as F


# noinspection PyAbstractClass,PyMethodMayBeStatic
class Flatten(nn.Module):
    def __init__(self, start_dim=0, end_dim=None):
        super(Flatten, self).__init__()
        if (start_dim > 0) and (end_dim is None):
            end_dim = start_dim
        elif end_dim is None:
            end_dim = -1
        self.start_dim = start_dim
        self.end_dim = end_dim

    def forward(self, x, **kwargs):
        return torch.flatten(x, start_dim=self.start_dim, end_dim=self.end_dim)


# noinspection PyAbstractClass,PyMethodMayBeStatic
class GlobalMaxPooling(nn.Module):
    def __init__(self):
        super(GlobalMaxPooling, self).__init__()

    def forward(self, x, **kwargs):
        if len(x.size()) == 2:
            x = torch.unsqueeze(x, 1)
            x = F.max_pool1d(x, kernel_size=x.size()[2:])
            x = torch.squeeze(x, 1)
        else:
            x = F.max_pool1d(x, kernel_size=x.size()[2:])
        x = torch.squeeze(x, 2)
        return x
