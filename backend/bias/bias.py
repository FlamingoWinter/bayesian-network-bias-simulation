from typing import Dict

import pandas as pd

from backend.candidates.candidate_group import CandidateGroup
from backend.recruiters.recruiter import Recruiter


# TODO - Calculate bias
#    For now we just calculate bias as the mean offset between the predicted score and the actual score.
#    Which isn't a valid calculation for bias.

class RecruiterBiasMeasurement:
    def __init__(self, mean_offset: float, mse: float):
        # TODO - Implement this class. This will be dependent on the bias metrics used.
        #    It might need to be an abc

        self.mean_offset: float = mean_offset
        self.mse: float = mse


def calculate_bias(scored_applications: pd.Series, candidates: CandidateGroup) -> RecruiterBiasMeasurement:
    # TODO - Implement this calculation correctly

    actual_scores = candidates.get_scores()
    offsets: pd.Series = scored_applications - actual_scores
    mse = (offsets ** 2).mean()
    return RecruiterBiasMeasurement(offsets.mean(), mse)


def print_bias_summary(bias_by_recruiter: Dict[Recruiter, RecruiterBiasMeasurement]) -> None:
    # TODO - Implement this function correctly
    print("")
    print("------ Bias Summary ------")

    for recruiter, recruiter_bias_measurement in bias_by_recruiter.items():
        print(f"Average offset from the mean for {recruiter.name} was {recruiter_bias_measurement.mean_offset}")
        print(f"Mean squared error for {recruiter.name} was {recruiter_bias_measurement.mse}")
    pass

    print("--------------------------")
    print("")
