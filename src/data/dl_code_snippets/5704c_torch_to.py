import torch
import torch.nn as nn


class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.linear = nn.Linear(10, 5).to(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

    def forward(self, x):
        return self.linear(x)


model = SimpleModel()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

input_data = torch.randn(2, 10).to(device)

output = model(input_data)
print("Output:", output)
