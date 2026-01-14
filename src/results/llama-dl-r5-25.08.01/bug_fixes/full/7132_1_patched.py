import torch
import torch.nn as nn
import torch.optim as optim


class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return torch.exp(self.linear(x))


class CustomLoss(nn.Module):
    def forward(self, outputs, targets):
        return torch.mean(torch.log(outputs - targets))


# Create data
torch.manual_seed(0)
x = torch.randn(10, 1)
y = torch.randn(10, 1)

model = SimpleModel()
optimizer = optim.SGD(model.parameters(), lr=0.01)
criterion = CustomLoss()

for epoch in range(100):
    optimizer.zero_grad()

    outputs = model(x)

    loss = criterion(outputs, y)
    if torch.isnan(loss):
        print("NaN loss encountered.")
        break
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item()}")

print("Training finished.")
