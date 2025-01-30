# Generate Simulation
from typing import List, Dict

from backend.bias.recruiter_bias_analysis import print_bias_summary, RecruiterBiasAnalysis
from backend.bias.threshold_score import threshold_score
from backend.candidates.candidate_group import CandidateGroup
from backend.candidates.generate_candidates import generate_candidate_group
from backend.network.bayesian_network import BayesianNetwork, Characteristic
from backend.network.generation.generate_network import generate_network
from backend.recruiters.logistic_regression_recruiter import LogisticRegressionRecruiter
from backend.recruiters.random_forest_recruiter import RandomForestRecruiter
from backend.recruiters.recruiter import Recruiter
from backend.utilities.time_function import time_function


@time_function("Simulating")
def simulate(candidate_group: CandidateGroup, recruiters: List[Recruiter], protected_characteristic: Characteristic):
    score_threshold = 0

    train_candidates, test_candidates = candidate_group.train_test_split(0.1)

    application_train = train_candidates.get_applications()
    score_train = train_candidates.get_scores()
    application_test = test_candidates.get_applications()

    bias_by_recruiter: Dict[Recruiter, RecruiterBiasAnalysis] = {}

    is_score_categorical: bool = candidate_group.network.characteristics[
                                     candidate_group.network.score_characteristic].type == "categorical"

    for recruiter in recruiters:
        is_recruiter_categorical: bool = recruiter.output_type == "categorical"

        if is_recruiter_categorical and not is_score_categorical:
            score_train = threshold_score(score_train, score_threshold)

        recruiter.train(application_train, score_train)
        bias_by_recruiter[recruiter] = RecruiterBiasAnalysis(recruiter,
                                                             test_candidates,
                                                             application_test,
                                                             protected_characteristic,
                                                             score_threshold)

    print_bias_summary(bias_by_recruiter)


if __name__ == "__main__":
    network: BayesianNetwork = generate_network()
    candidate_group: CandidateGroup = generate_candidate_group(network, 1_000_000)

    protected_characteristic = network.characteristics["0"]

    recruiters: List[Recruiter] = [RandomForestRecruiter(), LogisticRegressionRecruiter()]

    simulate(candidate_group, recruiters, protected_characteristic)
