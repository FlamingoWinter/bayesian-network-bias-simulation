import pandas as pd
import torch
from torch import nn, optim
from torch.utils.data import TensorDataset, DataLoader


def train_nn_model(model: nn.Module, optimiser: optim.Optimizer,
                   application_train: pd.DataFrame, score_train: pd.Series,
                   batch_size: int, epochs: int):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    X_train = torch.tensor(application_train.values, dtype=torch.float32)
    y_train = torch.tensor(score_train.values, dtype=torch.float32).unsqueeze(1)
    dataset = TensorDataset(X_train, y_train)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    loss_function = nn.BCEWithLogitsLoss()

    model.train()
    for _ in range(epochs):
        for batch_X, batch_y in dataloader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            optimiser.zero_grad()
            output = model(batch_X)
            loss = loss_function(output, batch_y)
            loss.backward()
            optimiser.step()
