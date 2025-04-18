from typing import List

import pandas as pd
import torch
from torch import nn, optim
from torch.utils.data import TensorDataset, DataLoader

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation
from backend.recruiters.recruiter import Recruiter


class DeepMLP(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int, depth: int):
        super(DeepMLP, self).__init__()

        layers = [nn.Linear(input_size, hidden_size), nn.ReLU()]

        for _ in range(depth - 1):
            layers += [nn.Linear(hidden_size, hidden_size), nn.ReLU()]

        layers += [nn.Linear(hidden_size, output_size)]

        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)


class DeepMLPRecruiter(Recruiter):
    @property
    def name(self):
        return "Deep MLP"

    @property
    def output_type(self):
        return "categorical"

    def __init__(self, mitigations: List[Mitigation], width=16, depth=16, epochs=10, lr=0.01, batch_size=512):
        super().__init__(mitigations)
        self.model = None
        self.width = width
        self.depth = depth
        self.epochs = epochs
        self.optimiser = None
        self.lr = lr
        self.batch_size = batch_size

    def train(self, application_train: pd.DataFrame, score_train: pd.Series):
        if self.model is None:
            self.model = DeepMLP(len(application_train.columns), self.width, 1, self.depth)
            self.optimiser = optim.Adam(self.model.parameters(), lr=self.lr)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)

        X_train = torch.tensor(application_train.values, dtype=torch.float32)
        y_train = torch.tensor(score_train.values, dtype=torch.float32).unsqueeze(1)
        dataset = TensorDataset(X_train, y_train)
        dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

        loss_function = nn.BCEWithLogitsLoss()

        self.model.train()
        for _ in range(self.epochs):
            for batch_X, batch_y in dataloader:
                batch_X, batch_y = batch_X.to(device), batch_y.to(device)
                self.optimiser.zero_grad()
                output = self.model(batch_X)
                loss = loss_function(output, batch_y)
                loss.backward()
                self.optimiser.step()

    def predict_scores(self, applications: pd.DataFrame) -> pd.Series:
        self.model.eval()
        X = torch.tensor(applications.values, dtype=torch.float32)
        predicted_scores = self.model(X).detach().numpy().flatten()
        return pd.Series(predicted_scores)
