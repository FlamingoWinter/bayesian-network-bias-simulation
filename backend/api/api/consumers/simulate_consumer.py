import json
from typing import Any
from typing import List

from backend.api.api.consumers.generic_consumer import GenericConsumer
from backend.api.cache import cache, get_network_from_cache
from backend.api.requestTypes.simulate_request import new_simulate_request, SimulateRequest
from backend.api.responseTypes.bias_response import \
    BiasResponse
from backend.applicants.applicants import Applicants
from backend.applicants.sample_applicants import sample_applicants
from backend.network.bayesian_network import BayesianNetwork
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
from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation
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
from backend.utilities.replace_nan import replace_nan


class SimulateConsumer(GenericConsumer):
    async def receive(self,
                      text_data: Any = None,
                      bytes_data: Any = None) -> None:
        request: SimulateRequest = new_simulate_request(**json.loads(text_data))
        network: BayesianNetwork = get_network_from_cache(self.session_key)
        candidate_group: Applicants = sample_applicants(network, request.candidates_to_generate * 2)

        await self.send_and_flush(f"{request.candidates_to_generate} Candidates Generated")

        recruiters: List[Recruiter] = [
            recruiter_string_to_recruiter(recruiter, request.recruiters[recruiter])
            for recruiter in request.recruiters.keys()]

        protected_characteristic = network.characteristics[request.protected_characteristic]
        bias_by_recruiter = simulate(candidate_group, recruiters, protected_characteristic,
                                     after_recruiter_generated=(
                                         lambda recruiter_name: self.send_and_flush(
                                             f"{recruiter_name} recruiter generated")
                                     ),
                                     after_mitigation_initialised=(
                                         lambda mitigation_name: self.send_and_flush(
                                             f"{mitigation_name} mitigation initialised")
                                     ))

        bias_response: BiasResponse = {recruiter.name: bias.to_response() for [recruiter, bias] in
                                       bias_by_recruiter.items()}

        cache(f"bias_{self.session_key}", replace_nan(bias_response))

        await self.close(code=1000)


def recruiter_string_to_recruiter(recruiter: str, mitigations: List[str]) -> Recruiter:
    recruiters_by_name = {
        "random_forest": RandomForestRecruiter,
        "logistic_regression": LogisticRegressionRecruiter,
        "transformer": EncoderOnlyTransformerRecruiter,
        "shallow_mlp": ShallowMLPRecruiter,
        "deep_mlp": DeepMLPRecruiter,
        "bayesian": BayesianRecruiter,
        "svm": SVMRecruiter,
    }

    if recruiter not in recruiters_by_name:
        raise f"Unknown recruiter {recruiter}"

    return recruiters_by_name[recruiter]([mitigation_string_to_mitigation(s) for s in mitigations])


def mitigation_string_to_mitigation(s: str) -> Mitigation:
    mitigations_by_name = {
        "no_mitigation": NoMitigation(),
        "satisfy_dp": SatisfyDemographicParity(),
        "satisfy_pp": SatisfyProportionalParity(),
        "optimise_fnr_fpr_accuracy": OptimiseForFNRFPRAccuracy(),
        "optimise_fnr_fpr": OptimiseForFNRAndFPREquality(),
        "optimise_fnr": OptimiseForFNREquality(),
        "optimise_fpr": OptimiseForFPREquality(),
        "optimise_fdr_for_accuracy": OptimiseForFDRFORAccuracy(),
        "optimise_fdr_for": OptimiseForFDRAndFOREquality(),
        "optimise_fdr": OptimiseForFDREquality(),
        "optimise_for": OptimiseForFOREquality(),
    }

    if s not in mitigations_by_name:
        raise f"Unknown mitigation {s}"

    return mitigations_by_name[s]
