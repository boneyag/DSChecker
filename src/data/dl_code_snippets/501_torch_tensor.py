import numpy as np
import torch


def calculate_accuracy(predictions, labels):
    if len(predictions) == 0 or len(labels) == 0:
        return None

    if len(predictions) != len(labels):
        return None

    correct = np.sum(predictions == labels)
    total = len(predictions)
    return correct / total


torch.manual_seed(0)
predictions = np.random.rand(1, 8)
labels = np.random.rand(
    8,
)
acc_tensor = torch.tensor(calculate_accuracy(predictions, labels))
