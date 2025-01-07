# Generate Simulation
from typing import List, Dict

import pandas as pd

from backend.bias.bias import calculate_bias, print_bias_summary, RecruiterBiasMeasurement
from backend.candidates.candidate_generation import generate_candidate_group
from backend.candidates.candidate_group import CandidateGroup
from backend.network.bayesian_network import BayesianNetwork
from backend.network.network_generation import generate_network
from backend.recruiters.linear_model_recruiter import LinearModelRecruiter
from backend.recruiters.recruiter import Recruiter
from backend.utilities.time_function import time_function


@time_function("Simulating network")
def simulate(network: BayesianNetwork, candidate_group: CandidateGroup, recruiters: List[Recruiter]):
    train_candidates, test_candidates = candidate_group.train_test_split(0.1)

    application_train = train_candidates.get_applications()
    score_train = train_candidates.get_scores()
    application_test = test_candidates.get_applications()

    score_predictions_by_recruiter: Dict[Recruiter, pd.Series] = {}
    bias_by_recruiter: Dict[Recruiter, RecruiterBiasMeasurement] = {}

    for recruiter in recruiters:
        recruiter.train(application_train, score_train)
        score_predictions_by_recruiter[recruiter] = recruiter.predict_scores(application_test)
        bias_by_recruiter[recruiter] = calculate_bias(score_predictions_by_recruiter[recruiter], test_candidates)

    print_bias_summary(bias_by_recruiter)


if __name__ == "__main__":
    network: BayesianNetwork = generate_network()
    candidate_group: CandidateGroup = generate_candidate_group(network, 10_000)
    recruiters: List[Recruiter] = [LinearModelRecruiter()]

    simulate(network, candidate_group, recruiters)
