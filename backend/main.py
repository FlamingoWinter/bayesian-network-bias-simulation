from typing import List

from backend.simulation.sample_applicants import Applicants
from backend.simulation.measure_bias.summary import print_bias_summary
from backend.simulation.build_network.bayesian_network import BayesianNetwork
from backend.simulation.build_network.generation.generate_categorical_network import (
    generate_random_categorical_network,
)
from backend.simulation.train_recruiters.mitigation.equalised_odds.optimise_for_fnr_and_fpr_equality import (
    OptimiseForFNRAndFPREquality,
)
from backend.simulation.train_recruiters.mitigation.equalised_odds.optimise_for_fnr_equality import (
    OptimiseForFNREquality,
)
from backend.simulation.train_recruiters.mitigation.equalised_odds.optimise_for_fnr_fpr_accuracy import (
    OptimiseForFNRFPRAccuracy,
)
from backend.simulation.train_recruiters.mitigation.equalised_odds.optimise_for_fpr_equality import (
    OptimiseForFPREquality,
)
from backend.simulation.train_recruiters.mitigation.predictive_parity.optimise_for_fdr_and_for_equality import (
    OptimiseForFDRAndFOREquality,
)
from backend.simulation.train_recruiters.mitigation.predictive_parity.optimise_for_fdr_equality import (
    OptimiseForFDREquality,
)
from backend.simulation.train_recruiters.mitigation.predictive_parity.optimise_for_fdr_for_accuracy import (
    OptimiseForFDRFORAccuracy,
)
from backend.simulation.train_recruiters.mitigation.predictive_parity.optimise_for_for_equality import (
    OptimiseForFOREquality,
)
from backend.simulation.train_recruiters.mitigation.no_mitigation import NoMitigation
from backend.simulation.train_recruiters.mitigation.demographic_parity import (
    SatisfyDemographicParity,
)
from backend.simulation.train_recruiters.mitigation.proportional_parity import (
    SatisfyProportionalParity,
)
from backend.simulation.train_recruiters.models.bayesian_recruiter import BayesianRecruiter
from backend.simulation.train_recruiters.models.deep_mlp_recruiter import DeepMLPRecruiter
from backend.simulation.train_recruiters.models.encoder_only_transformer_recruiter import (
    EncoderOnlyTransformerRecruiter,
)
from backend.simulation.train_recruiters.models.logistic_regression_recruiter import (
    LogisticRegressionRecruiter,
)
from backend.simulation.train_recruiters.models.random_forest_recruiter import (
    RandomForestRecruiter,
)
from backend.simulation.train_recruiters.models.shallow_mlp_recruiter import (
    ShallowMLPRecruiter,
)
from backend.simulation.train_recruiters.models.svm_recruiter import SVMRecruiter
from backend.simulation.train_recruiters.recruiter import Recruiter
from backend.simulation.simulate import simulate

if __name__ == "__main__":
    network: BayesianNetwork = generate_random_categorical_network(20)

    candidate_group: Applicants = network.sample_applicants(10_000)

    protected_characteristic = list(network.characteristics.values())[0]

    recruiters: List[Recruiter] = [
        RandomForestRecruiter(
            [
                NoMitigation(),
                SatisfyDemographicParity(),
                SatisfyProportionalParity(),
                OptimiseForFNRFPRAccuracy(),
                OptimiseForFNRAndFPREquality(),
                OptimiseForFNREquality(),
                OptimiseForFPREquality(),
                OptimiseForFDRFORAccuracy(),
                OptimiseForFDRAndFOREquality(),
                OptimiseForFDREquality(),
                OptimiseForFOREquality(),
            ]
        ),
        BayesianRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]
        ),
        ShallowMLPRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]
        ),
        DeepMLPRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]
        ),
        EncoderOnlyTransformerRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]
        ),
        LogisticRegressionRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]
        ),
        SVMRecruiter(
            [NoMitigation(), SatisfyDemographicParity(), SatisfyProportionalParity()]
        ),
    ]

    bias_by_recruiter = simulate(candidate_group, recruiters, protected_characteristic)
    print_bias_summary(bias_by_recruiter)
