from typing import List

from backend.applicants.applicants import Applicants
from backend.bias.print_bias_summary import print_bias_summary
from backend.network.bayesian_network import BayesianNetwork
from backend.network.generation.generate_categorical_network import generate_random_categorical_network
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
from backend.recruiters.categorical_output.bayesian_recruiter import BayesianRecruiter
from backend.recruiters.categorical_output.deep_mlp_recruiter import DeepMLPRecruiter
from backend.recruiters.categorical_output.encoder_only_transformer_recruiter import EncoderOnlyTransformerRecruiter
from backend.recruiters.categorical_output.logistic_regression_recruiter import LogisticRegressionRecruiter
from backend.recruiters.categorical_output.random_forest_recruiter import RandomForestRecruiter
from backend.recruiters.categorical_output.shallow_mlp_recruiter import ShallowMLPRecruiter
from backend.recruiters.categorical_output.svm_recruiter import SVMRecruiter
from backend.recruiters.recruiter import Recruiter
from backend.simulate import simulate

if __name__ == "__main__":
    network: BayesianNetwork = generate_random_categorical_network(20)

    candidate_group: Applicants = network.sample_applicants(10_000)

    protected_characteristic = list(network.characteristics.values())[0]

    recruiters: List[Recruiter] = [
        RandomForestRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity(),
             OptimiseForFNRFPRAccuracy(), OptimiseForFNRAndFPREquality(), OptimiseForFNREquality(),
             OptimiseForFPREquality(),
             OptimiseForFDRFORAccuracy(), OptimiseForFDRAndFOREquality(), OptimiseForFDREquality(),
             OptimiseForFOREquality(),
             ]),

        BayesianRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        ShallowMLPRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        DeepMLPRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        EncoderOnlyTransformerRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        LogisticRegressionRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),
        SVMRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]),

    ]

    bias_by_recruiter = simulate(candidate_group, recruiters, protected_characteristic)
    print_bias_summary(bias_by_recruiter)
