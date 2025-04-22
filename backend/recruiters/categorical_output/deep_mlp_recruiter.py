from typing import List

import pandas as pd
import torch
from torch import nn, optim

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation
from backend.recruiters.categorical_output.train_nn_model import train_nn_model
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
        train_nn_model(self.model, self.optimiser, application_train, score_train, self.batch_size, self.epochs)

    def predict_scores(self, applications: pd.DataFrame) -> pd.Series:
        self.model.eval()
        X = torch.tensor(applications.values, dtype=torch.float32)
        predicted_scores = self.model(X).detach().numpy().flatten()
        return pd.Series(predicted_scores)
