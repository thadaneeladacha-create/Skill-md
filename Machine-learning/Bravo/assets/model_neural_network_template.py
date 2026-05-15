"""
Neural Network Template (PyTorch)
ตัวอย่าง feed-forward network สำหรับ tabular data
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


# ---------- กำหนดค่า ----------
INPUT_DIM = 20          # จำนวน features
HIDDEN_DIM = 64
OUTPUT_DIM = 2          # จำนวน class (classification) หรือ 1 (regression)
LEARNING_RATE = 1e-3
BATCH_SIZE = 64
EPOCHS = 50
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ---------- สร้าง Model ----------
class SimpleNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, dropout=0.2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x):
        return self.net(x)


# ---------- เตรียม DataLoader ----------
def make_dataloader(X, y, batch_size=BATCH_SIZE, shuffle=True):
    """แปลง numpy/pandas เป็น DataLoader"""
    X_t = torch.tensor(X, dtype=torch.float32)
    y_t = torch.tensor(y, dtype=torch.long)  # ใช้ float สำหรับ regression
    dataset = TensorDataset(X_t, y_t)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


# ---------- Training Loop ----------
def train_model(model, train_loader, val_loader, epochs=EPOCHS, lr=LEARNING_RATE):
    model = model.to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()  # ใช้ MSELoss สำหรับ regression

    history = {"train_loss": [], "val_loss": []}

    for epoch in range(epochs):
        # ---- Training ----
        model.train()
        train_loss = 0.0
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(DEVICE), y_batch.to(DEVICE)
            optimizer.zero_grad()
            preds = model(X_batch)
            loss = criterion(preds, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * X_batch.size(0)
        train_loss /= len(train_loader.dataset)

        # ---- Validation ----
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.to(DEVICE), y_batch.to(DEVICE)
                preds = model(X_batch)
                loss = criterion(preds, y_batch)
                val_loss += loss.item() * X_batch.size(0)
        val_loss /= len(val_loader.dataset)

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)

        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1:3d}  train_loss: {train_loss:.4f}  val_loss: {val_loss:.4f}")

    return model, history


# ---------- ตัวอย่างการเรียกใช้ ----------
# model = SimpleNN(INPUT_DIM, HIDDEN_DIM, OUTPUT_DIM)
# train_loader = make_dataloader(X_train_processed, y_train.values)
# val_loader = make_dataloader(X_val_processed, y_val.values, shuffle=False)
# model, history = train_model(model, train_loader, val_loader)
