import json
from typing import Any
from typing import List, Dict

from backend.api.api.cache_network import get_network_from_cache
from backend.api.api.consumers.generic_consumer import GenericConsumer
from backend.api.cache.cache import cache
from backend.api.requestTypes.simulate_request import new_simulate_request, SimulateRequest
from backend.api.responseTypes.recruiterBiasAnalysisResponse.biasResponse import \
    BiasResponse
from backend.bias.recruiter_bias_analysis import RecruiterBiasAnalysis
from backend.candidates.candidate_group import CandidateGroup
from backend.candidates.generate_candidates import generate_candidate_group
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
from backend.utilities.replace_nan import replace_nan


def recruiter_string_to_recruiter(recruiter: str, mitigations: List[str]) -> Recruiter:
    recruiter_map = {
        "random_forest": RandomForestRecruiter,
        "logistic_regression": LogisticRegressionRecruiter,
        "transformer": EncoderOnlyTransformerRecruiter,
        "shallow_mlp": ShallowMLPRecruiter,
        "deep_mlp": DeepMLPRecruiter,
        "bayesian": BayesianRecruiter,
        "svm": SVMRecruiter,
    }

    if recruiter not in recruiter_map:
        raise ValueError(f"Unknown recruiter type: {recruiter}")

    return recruiter_map[recruiter]([mitigation_string_to_mitigation(s) for s in mitigations])


def mitigation_string_to_mitigation(s: str) -> Mitigation:
    mitigation_map = {
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

    if s not in mitigation_map:
        raise ValueError(f"Unknown mitigation: {s}")

    return mitigation_map[s]


class SimulateConsumer(GenericConsumer):
    session_key: str

    async def receive(self,
                      text_data: Any = None,
                      bytes_data: Any = None) -> None:
        request: SimulateRequest = new_simulate_request(**json.loads(text_data))

        network: BayesianNetwork = get_network_from_cache(self.session_key)

        candidate_group: CandidateGroup = generate_candidate_group(network, request.candidates_to_generate * 2)

        await self.send_and_flush(f"{request.candidates_to_generate} Candidates Generated")

        recruiters: List[Recruiter] = [
            recruiter_string_to_recruiter(recruiter, request.recruiters[recruiter])
            for recruiter in request.recruiters.keys()]

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

        protected_characteristic = network.characteristics[request.protected_characteristic]

        for recruiter in recruiters:
            if recruiter.name == "Bayesian Recruiter":
                application_test, application_train, application_holdout = application_test_raw, application_train_raw, application_holdout_raw
            else:
                application_test, application_train, application_holdout = application_test_one_hot, application_train_one_hot, application_holdout_one_hot

            recruiter.train(application_train, score_train)

            groups_train = train_candidates.characteristics[protected_characteristic.name].reset_index(drop=True)
            groups_holdout = holdout_candidates.characteristics[protected_characteristic.name].reset_index(drop=True)

            recruiter.initalise_mitigation(score_train, groups_train,
                                           score_holdout, application_holdout, groups_holdout,
                                           )

            bias_by_recruiter[recruiter] = RecruiterBiasAnalysis(recruiter,
                                                                 test_candidates,
                                                                 application_test,
                                                                 protected_characteristic,
                                                                 )
            await self.send_and_flush(f"Trained recruiter: {recruiter.name}")

        bias_response: BiasResponse = {recruiter.name: bias.to_response() for [recruiter, bias] in
                                       bias_by_recruiter.items()}

        cache(f"bias_{self.session_key}", replace_nan(bias_response))

        await self.close(code=1000)
