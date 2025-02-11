import pandas as pd
from sklearn.metrics import r2_score

from backend.network.bayesian_network import Characteristic


class ContinuousRecruiterBiasAnalysis:
    def __init__(self, applications: pd.DataFrame, protected_characteristic: Characteristic):
        # Requires that application has a categorical column "group" denoting whether it is in the biased group,
        # a continuous column "predicted_score" and a continuous column "actual_score",
        # where a higher value is positive (more competent, more likely to be accepted).
        super().__init__()
        self.r2 = r2_score(applications["actual_score"], applications["predicted_score"])

    def print_summary(self):
        print(f"Performance:")
        print(f"---")
        print(f"R2: {self.r2}")
        print(f"---")

    def to_response(self):
        # Todo
        return {}
