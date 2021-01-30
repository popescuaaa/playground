from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch
import numpy as np

DATASET_CONFIG = ['Open' 'High' 'Low' 'Close' 'Adj_Close' 'Volume']


class StockDataset(Dataset):
    def __init__(self, seq_len=10, normalize=False):
        # sequence len is limited by numpy at 32

        self.row_data = np.loadtxt('./stock_data.csv', delimiter=',', dtype=np.str)

        self.data = [float(e[3]) for e in self.row_data[1:]]
        tensor_like = []

        for idx in range(0, len(self.data) - seq_len):
            tensor_like.append(self.data[idx: idx + seq_len])

        self.data = torch.FloatTensor(tensor_like)
        self.len = self.data.shape[0]
        self.mean = self.data.mean()
        self.std = torch.std(self.data)

        if normalize:
            self.data = self.normalize()

    def normalize(self):
        normalized_data = (self.data - self.mean) / self.std
        return normalized_data

    def denormalize(self):
        denormalized_data = self.data * self.std + self.mean
        return denormalized_data

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        return self.data[idx]


class StockDatasetDeltas(Dataset):
    """
    Dataset return a sequence: [ start_value : sequence_deltas ]
    Actual sequence len: seq_len - 1
    """

    def __init__(self, seq_len=10):
        # sequence len is limited by numpy at 32

        self.row_data = np.loadtxt('./stock_data.csv', delimiter=',', dtype=np.str)

        self.data = [float(e[3]) for e in self.row_data[1:]]
        tensor_like = []

        for idx in range(0, len(self.data) - seq_len):
            deltas = np.subtract(np.array(self.data[idx: idx + seq_len][1:]),
                                 np.array(self.data[idx: idx + seq_len][:-1]))

            deltas = np.concatenate([np.array([self.data[idx: idx + seq_len][0]]),
                                     deltas])

            tensor_like.append(deltas)

        self.data = torch.FloatTensor(tensor_like)
        self.len = self.data.shape[0]
        self.mean = self.data.mean()
        self.std = torch.std(self.data)

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        return self.data[idx]


def test_stock_dataset() -> None:
    ds = StockDataset()
    dl = DataLoader(ds, batch_size=5, shuffle=True, num_workers=10)
    for i, real in enumerate(dl):
        print('Index: {} data {}'.format(i, real))
        break

    ds = StockDataset(normalize=True)
    dl = DataLoader(ds, batch_size=10, shuffle=True, num_workers=10)
    for i, batch in enumerate(dl):
        print('Index: {} data {}'.format(i, batch))
        break


def test_deltas_stock_dataset() -> None:
    ds = StockDatasetDeltas()
    dl = DataLoader(ds, batch_size=5, shuffle=False, num_workers=10)
    for i, real in enumerate(dl):
        print('Index: {} data {}'.format(i, real))
        break


if __name__ == '__main__':
    test_deltas_stock_dataset()
