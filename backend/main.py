from typing import List, Dict

from backend.bias.recruiter_bias_analysis import print_bias_summary, RecruiterBiasAnalysis
from backend.bias.threshold_score import threshold_score
from backend.candidates.candidate_group import CandidateGroup
from backend.candidates.generate_candidates import generate_candidate_group
from backend.network.bayesian_network import BayesianNetwork, Characteristic
from backend.network.generation.generate_network import generate_network
from backend.recruiters.categorical_bias_mitigation.approach_equalised_odds.optimise_for_fnr_fpr_accuracy import \
    OptimiseForFNRFPRAccuracy
from backend.recruiters.categorical_output.random_forest_recruiter import RandomForestRecruiter
from backend.recruiters.recruiter import Recruiter
from backend.utilities.time_function import time_function


@time_function("Simulating")
def simulate(candidate_group: CandidateGroup, recruiters: List[Recruiter], protected_characteristic: Characteristic):
    score_threshold = 0

    train_candidates, holdout_candidates, test_candidates = candidate_group.random_split([0.5, 0.25, 0.25])

    application_train_one_hot = train_candidates.get_applications(one_hot_encode_categorical_variables=True)
    application_test_one_hot = test_candidates.get_applications(one_hot_encode_categorical_variables=True)
    application_holdout_one_hot = holdout_candidates.get_applications(one_hot_encode_categorical_variables=True)
    application_train_raw = train_candidates.get_applications()
    application_test_raw = test_candidates.get_applications()
    application_holdout_raw = holdout_candidates.get_applications()

    score_train = train_candidates.get_scores()
    score_holdout = holdout_candidates.get_scores()

    bias_by_recruiter: Dict[Recruiter, RecruiterBiasAnalysis] = {}

    is_score_categorical: bool = (candidate_group.network.characteristics[
                                      candidate_group.network.score_characteristic].type == "categorical")

    for recruiter in recruiters:
        is_recruiter_categorical: bool = (recruiter.output_type == "categorical")

        if is_recruiter_categorical and not is_score_categorical:
            score_train = threshold_score(score_train, score_threshold)

        if recruiter.name == "Bayesian Recruiter":
            application_test, application_train, application_holdout = application_test_raw, application_train_raw, application_holdout_raw
        else:
            application_test, application_train, application_holdout = application_test_one_hot, application_train_one_hot, application_holdout_one_hot

        recruiter.train(application_train, score_train)

        groups_train = train_candidates.characteristics[protected_characteristic.name]
        groups_holdout = holdout_candidates.characteristics[protected_characteristic.name]
        groups_test = test_candidates.characteristics[protected_characteristic.name]

        print("train group proportions", groups_train.value_counts(normalize=True).sort_index())
        print("holdout group proportions", groups_holdout.value_counts(normalize=True).sort_index())
        print("test group proportions", groups_test.value_counts(normalize=True).sort_index())

        recruiter.initalise_mitigation(score_train, groups_train,
                                       score_holdout, application_holdout, groups_holdout,
                                       )

        bias_by_recruiter[recruiter] = RecruiterBiasAnalysis(recruiter,
                                                             test_candidates,
                                                             application_test,
                                                             protected_characteristic,
                                                             score_threshold)

    print_bias_summary(bias_by_recruiter)


if __name__ == "__main__":
    network: BayesianNetwork = generate_network()
    candidate_group: CandidateGroup = generate_candidate_group(network, 10_000)

    protected_characteristic = list(network.characteristics.values())[0]

    recruiters: List[Recruiter] = [RandomForestRecruiter(OptimiseForFNRFPRAccuracy())]

    simulate(candidate_group, recruiters, protected_characteristic)
