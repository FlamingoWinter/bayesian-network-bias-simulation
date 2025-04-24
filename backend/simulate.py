from typing import List, Dict, Callable, Any

from backend.applicants.applicants import Applicants
from backend.bias.recruiter_bias_analysis import RecruiterBiasAnalysis
from backend.network.bayesian_network import Characteristic
from backend.recruiters.recruiter import Recruiter
from backend.utilities.time_function import time_function


@time_function("Simulating")
def simulate(applicants: Applicants, recruiters: List[Recruiter], protected_characteristic: Characteristic,
             after_recruiter_generated: Callable[[str], Any] = lambda _: None,
             after_mitigation_initialised: Callable[[str], Any] = lambda _: None) -> \
        dict[Recruiter, RecruiterBiasAnalysis]:
    train_candidates, mitigation_candidates, test_candidates = applicants.random_split([0.5, 0.25, 0.25])

    application_train_one_hot = train_candidates.get_applications(one_hot_encode_categorical_variables=True)
    application_test_one_hot = test_candidates.get_applications(one_hot_encode_categorical_variables=True)
    application_mitigation_one_hot = mitigation_candidates.get_applications(one_hot_encode_categorical_variables=True)
    application_train_raw = train_candidates.get_applications()
    application_test_raw = test_candidates.get_applications()
    application_mitigation_raw = mitigation_candidates.get_applications()

    score_train = train_candidates.get_scores()
    score_holdout = mitigation_candidates.get_scores()

    bias_by_recruiter: Dict[Recruiter, RecruiterBiasAnalysis] = {}

    for recruiter in recruiters:
        if recruiter.name == "Bayesian Recruiter":
            application_test, application_train, application_holdout = application_test_raw, application_train_raw, application_mitigation_raw
        else:
            application_test, application_train, application_holdout = application_test_one_hot, application_train_one_hot, application_mitigation_one_hot

        recruiter.train(application_train, score_train)

        groups_train = train_candidates.characteristic_instances[protected_characteristic.name].reset_index(drop=True)

        groups_holdout = mitigation_candidates.characteristic_instances[protected_characteristic.name].reset_index(
            drop=True)

        recruiter.initalise_mitigation(score_train, groups_train,
                                       score_holdout, application_holdout, groups_holdout,
                                       after_mitigation_initialised
                                       )

        bias_by_recruiter[recruiter] = RecruiterBiasAnalysis(recruiter,
                                                             test_candidates,
                                                             application_test,
                                                             protected_characteristic)
        after_recruiter_generated(recruiter.name)

    return bias_by_recruiter
