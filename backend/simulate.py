from typing import List, Dict

from backend.bias.recruiter_bias_analysis import RecruiterBiasAnalysis
from backend.candidates.candidate_group import CandidateGroup
from backend.network.bayesian_network import Characteristic
from backend.recruiters.recruiter import Recruiter
from backend.utilities.time_function import time_function


@time_function("Simulating")
def simulate(candidate_group: CandidateGroup, recruiters: List[Recruiter], protected_characteristic: Characteristic) -> \
        dict[Recruiter, RecruiterBiasAnalysis]:
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
                                                             protected_characteristic)

    return bias_by_recruiter
