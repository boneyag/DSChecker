import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleModel(nn.Module):
    def __init__(self, dropout_prob=0.5):
        super(SimpleModel, self).__init__()
        self.linear1 = nn.Linear(10, 20)
        self.dropout = nn.Dropout(dropout_prob)
        self.linear2 = nn.Linear(20, 2)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.dropout(x)
        x = self.linear2(x)
        return x


def evaluate_accuracy(net, data_iter):
    correct = 0
    total = 0
    with torch.no_grad():
        for X, y in data_iter:
            outputs = net(X)
            _, predicted = torch.max(outputs.data, 1)
            total += y.size(0)
            correct += (predicted == y).sum().item()
    return correct / total


torch.manual_seed(0)
data_iter = [(torch.randn(10, 10), torch.randint(0, 2, (10,))) for _ in range(10)]

model = SimpleModel()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()

for epoch in range(50):
    model.train()
    for X, y in data_iter:
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()

accuracy_eval = evaluate_accuracy(model, data_iter)
print(f"Accuracy (eval): {accuracy_eval}")
