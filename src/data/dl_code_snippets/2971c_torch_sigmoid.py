import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset

data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
train_loader = DataLoader(dataset=train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=32, shuffle=False)


class BinaryClassifier(nn.Module):
    def __init__(self, input_size):
        super(BinaryClassifier, self).__init__()
        self.linear = nn.Linear(input_size, 1)

    def forward(self, x):
        return self.linear(x)


input_size = X_train_tensor.shape[1]
model = BinaryClassifier(input_size)
loss_fn = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


def training_step(model, batch, loss_fn, optimizer):
    x, y = batch
    y_logits = model(x)
    loss = loss_fn(y_logits, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss.item()


def validation_step(model, batch, loss_fn):
    x, y = batch
    y_logits = model(x)
    loss = loss_fn(y_logits, y)

    y_score = torch.sigmoid(y_logits)
    y_pred = (y_score > 0.5).float()
    accuracy = (y_pred == y).float().mean()

    return loss.item(), accuracy.item()


num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    train_loss = 0.0
    for batch in train_loader:
        train_loss += training_step(model, batch, loss_fn, optimizer)
    train_loss /= len(train_loader)

    model.eval()
    val_loss = 0.0
    val_accuracy = 0.0
    with torch.no_grad():
        for batch in test_loader:
            loss, accuracy = validation_step(model, batch, loss_fn)
            val_loss += loss
            val_accuracy += accuracy
    val_loss /= len(test_loader)
    val_accuracy /= len(test_loader)

    if (epoch + 1) % 10 == 0:
        print(
            f"Epoch [{epoch + 1}/{num_epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.4f}"
        )
