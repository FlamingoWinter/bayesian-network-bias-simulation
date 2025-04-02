from typing import List, Dict

from backend.bias.recruiter_bias_analysis import print_bias_summary, RecruiterBiasAnalysis
from backend.bias.threshold_score import threshold_score
from backend.candidates.candidate_group import CandidateGroup
from backend.candidates.generate_candidates import generate_candidate_group
from backend.network.bayesian_network import BayesianNetwork, Characteristic
from backend.network.generation.generate_network import generate_network
from backend.recruiters.categorical_bias_mitigation.approach_equalised_odds.optimise_for_fnr_and_fpr_equality import \
    OptimiseForFNRAndFPREquality
from backend.recruiters.categorical_bias_mitigation.approach_equalised_odds.optimise_for_fnr_equality import \
    OptimiseForFNREquality
from backend.recruiters.categorical_bias_mitigation.approach_equalised_odds.optimise_for_fnr_fpr_accuracy import \
    OptimiseForFNRFPRAccuracy
from backend.recruiters.categorical_bias_mitigation.approach_equalised_odds.optimise_for_fpr_equality import \
    OptimiseForFPREquality
from backend.recruiters.categorical_bias_mitigation.approach_predictive_parity.optimise_for_fdr_and_for_equality import \
    OptimiseForFDRAndFOREquality
from backend.recruiters.categorical_bias_mitigation.approach_predictive_parity.optimise_for_fdr_equality import \
    OptimiseForFDREquality
from backend.recruiters.categorical_bias_mitigation.approach_predictive_parity.optimise_for_fdr_for_accuracy import \
    OptimiseForFDRFORAccuracy
from backend.recruiters.categorical_bias_mitigation.approach_predictive_parity.optimise_for_for_equality import \
    OptimiseForFOREquality
from backend.recruiters.categorical_bias_mitigation.no_mitigation import NoMitigation
from backend.recruiters.categorical_bias_mitigation.satisfy_demographic_parity import SatisfyDemographicParity
from backend.recruiters.categorical_bias_mitigation.satisfy_proportional_parity import SatisfyProportionalParity
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

        groups_train = train_candidates.characteristics[protected_characteristic.name].reset_index(drop=True)
        print("Group Proportions", list(groups_train.value_counts(normalize=True)))

        groups_holdout = holdout_candidates.characteristics[protected_characteristic.name].reset_index(drop=True)

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

    recruiters: List[Recruiter] = [
        RandomForestRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity(),
             OptimiseForFNRFPRAccuracy(), OptimiseForFNRAndFPREquality(), OptimiseForFNREquality(),
             OptimiseForFPREquality(),
             OptimiseForFDRFORAccuracy(), OptimiseForFDRAndFOREquality(), OptimiseForFDREquality(),
             OptimiseForFOREquality(),
             ]),

        # approx 40s - 2 minutes

        # RandomForestRecruiter(
        #     [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        # BayesianRecruiter(
        #     [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        # ShallowMLPRecruiter(
        #     [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        # DeepMLPRecruiter(
        #     [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        # EncoderOnlyTransformerRecruiter(
        #     [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        # LogisticRegressionRecruiter(
        #     [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        # SVMRecruiter(
        #     [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),

        # approx 20-40 seconds
    ]

    simulate(candidate_group, recruiters, protected_characteristic)
