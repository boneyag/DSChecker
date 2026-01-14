import torch
import torch.nn as nn

torch.manual_seed(0)

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.cov1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(16 * 13 * 13, 2)

    def forward(self, x):
        x = self.pool(torch.relu(self.cov1(x)))
        x = self.flatten(x)
        x = self.fc1(x)
        return x

model = SimpleCNN()
input = torch.randn(1, 1, 28, 28)
output = model(input)
print(output.size())
