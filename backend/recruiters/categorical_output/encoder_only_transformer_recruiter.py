from typing import List

import pandas as pd
import torch
from torch import nn, optim

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation
from backend.recruiters.categorical_output.train_nn_model import train_nn_model
from backend.recruiters.recruiter import Recruiter


class Transformer(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int,
                 depth: int, num_heads: int, dropout=0.1):
        super(Transformer, self).__init__()

        self.first_layer = nn.Linear(input_size, hidden_size)
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=hidden_size, nhead=num_heads, dropout=dropout, batch_first=True),
            num_layers=depth
        )

        self.output_layer = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        first_layer_output = self.first_layer(x)
        encoder_output = self.encoder(first_layer_output)
        return self.output_layer(encoder_output)


class EncoderOnlyTransformerRecruiter(Recruiter):
    @property
    def name(self):
        return "Encoder-Only Transformer"

    @property
    def output_type(self):
        return "categorical"

    def __init__(self, mitigations: List[Mitigation], width=16, depth=4, epochs=3, lr=1e-4, batch_size=512,
                 num_heads=2):
        super().__init__(mitigations)
        self.model = None
        self.width = width
        self.depth = depth
        self.num_heads = num_heads
        self.epochs = epochs
        self.optimiser = None
        self.lr = lr
        self.batch_size = batch_size

    def train(self, application_train: pd.DataFrame, score_train: pd.Series):
        if self.model is None:
            self.model = Transformer(len(application_train.columns), self.width, 1,
                                     self.depth, self.num_heads)
            self.optimiser = optim.Adam(self.model.parameters(), lr=self.lr)

        train_nn_model(self.model, self.optimiser, application_train, score_train, self.batch_size, self.epochs)

    def predict_scores(self, applications: pd.DataFrame) -> pd.Series:
        self.model.eval()
        X = torch.tensor(applications.values, dtype=torch.float32)
        predicted_scores = self.model(X).detach().numpy().flatten()
        return pd.Series(predicted_scores)
