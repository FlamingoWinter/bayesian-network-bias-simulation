from datetime import datetime
from typing import List

from backend.experiments.helpers.save_to_db import save_run_to_db, save_recruiter_run_to_db
from backend.simulation.build_network.generation.choose_characteristics import (
    choose_application,
)
from backend.experiments.helpers.setup_experiment import setup_experiment
from backend.simulation.train_recruiters.mitigation.no_mitigation import NoMitigation
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
from backend.utils.time_function import time_function


@time_function("Network Structure Conditions Run")
def network_structure_conditions_run():
    try:
        (
            start_time,
            engine,
            network,
            applicants,
            score_characteristic_name,
            protected_characteristic_name,
        ) = setup_experiment()
    except Exception:
        return network_structure_conditions_run()

    network_creation_time = datetime.now()

    for condition in [1, 2, 3, 4]:
        condition_start_time = datetime.now()
        network.application_characteristics = choose_application(
            network.model.to_directed(),
            condition,
            score_characteristic_name,
            protected_characteristic_name,
        )

        recruiters: List[Recruiter] = [
            RandomForestRecruiter([NoMitigation()]),
            BayesianRecruiter([NoMitigation()]),
            ShallowMLPRecruiter([NoMitigation()]),
            DeepMLPRecruiter([NoMitigation()]),
            EncoderOnlyTransformerRecruiter([NoMitigation()]),
            LogisticRegressionRecruiter([NoMitigation()]),
            SVMRecruiter([NoMitigation()]),
        ]

        protected_characteristic = network.characteristics[
            protected_characteristic_name
        ]
        bias_by_recruiter = simulate(applicants, recruiters, protected_characteristic)

        db_run_id = save_run_to_db(
            engine,
            network,
            applicants,
            protected_characteristic_name,
            condition,
            datetime.now() - condition_start_time + network_creation_time - start_time,
        )
        for bias, recruiter_bias_analysis in bias_by_recruiter.items():
            save_recruiter_run_to_db(engine, db_run_id, recruiter_bias_analysis)


if __name__ == "__main__":
    while True:
        try:
            network_structure_conditions_run()
        except Exception:
            pass
