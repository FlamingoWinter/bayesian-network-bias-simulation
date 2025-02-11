import json
from typing import Any
from typing import List, Dict
from urllib.parse import parse_qs

import pymc as pm
from channels.generic.websocket import AsyncWebsocketConsumer
from pgmpy.models import BayesianNetwork as PgBn

from backend.api.cache.cache import from_cache, cache
from backend.api.requestTypes.SimulateRequest import new_simulate_request
from backend.api.responseTypes.recruiterBiasAnalysisResponse.biasResponse import \
    BiasResponse
from backend.bias.recruiter_bias_analysis import print_bias_summary, RecruiterBiasAnalysis
from backend.bias.threshold_score import threshold_score
from backend.candidates.candidate_group import CandidateGroup
from backend.candidates.generate_candidates import generate_candidate_group
from backend.network.bayesian_network import BayesianNetwork
from backend.recruiters.random_forest_recruiter import RandomForestRecruiter
from backend.recruiters.recruiter import Recruiter
from backend.utilities.replace_nan import replace_nan


def recruiter_string_to_recruiter(s: str) -> Recruiter:
    return RandomForestRecruiter()
    # TODO: Implement mapping from strings to recruiters


class SimulateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope.get("query_string", b"").decode("utf-8")

        query_params = parse_qs(query_string)
        self.session_key = query_params.get("session_key", [None])[0]

        self.room_name = "simulate"

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self,
                      text_data: Any = None,
                      bytes_data: Any = None) -> None:
        simulate_request = new_simulate_request(**json.loads(text_data))

        network: BayesianNetwork = from_cache(f"network_{self.session_key}",
                                              "network")
        if network.model_type == "pgmpy":
            network.model.__class__ = PgBn
        else:
            network.model.__class__ = pm.Model

        candidate_group: CandidateGroup = generate_candidate_group(network, simulate_request.candidates_to_generate)

        await self.send(text_data=json.dumps({
            'message': f"{simulate_request.candidates_to_generate} Candidates Generated"
        }))

        recruiters: List[Recruiter] = [recruiter_string_to_recruiter(s) for s in simulate_request.recruiters]

        train_candidates, test_candidates = candidate_group.train_test_split(
            test_size=(1 - simulate_request.train_proportion))

        application_train = train_candidates.get_applications()
        score_train = train_candidates.get_scores()
        application_test = test_candidates.get_applications()

        bias_by_recruiter: Dict[Recruiter, RecruiterBiasAnalysis] = {}

        protected_characteristic = network.characteristics[simulate_request.protected_characteristic]

        for recruiter in recruiters:
            if simulate_request.categorical_or_continuous == "continuous":
                if recruiter.output_type == "categorical":
                    score_train = threshold_score(score_train, simulate_request.score_threshold)
            recruiter.train(application_train, score_train)
            if simulate_request.categorical_or_continuous == "continuous":
                bias_by_recruiter[recruiter] = RecruiterBiasAnalysis(recruiter,
                                                                     test_candidates,
                                                                     application_test,
                                                                     protected_characteristic,
                                                                     simulate_request.score_threshold
                                                                     )
            else:
                bias_by_recruiter[recruiter] = RecruiterBiasAnalysis(recruiter,
                                                                     test_candidates,
                                                                     application_test,
                                                                     protected_characteristic,
                                                                     )
            await self.send(text_data=json.dumps({
                'message': f"Trained recruiter: {recruiter.name}"
            }))

        bias_response: BiasResponse = {recruiter.name: bias.to_response() for [recruiter, bias] in
                                       bias_by_recruiter.items()}

        cache(f"bias_{self.session_key}", replace_nan(bias_response))

        print_bias_summary(bias_by_recruiter)

        await self.close(code=1000)
