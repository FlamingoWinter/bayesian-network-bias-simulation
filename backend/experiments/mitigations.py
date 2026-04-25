from datetime import datetime
from typing import List

from backend.experiments.helpers.save_to_db import save_run_to_db, save_recruiter_run_to_db
from backend.simulation.build_network.generation.choose_characteristics import (
    choose_application,
)
from backend.experiments.helpers.setup_experiment import setup_experiment
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
from backend.simulation.train_recruiters.models.random_forest_recruiter import (
    RandomForestRecruiter,
)
from backend.simulation.train_recruiters.recruiter import Recruiter
from backend.simulation.simulate import simulate
from backend.utils.time_function import time_function


@time_function("Mitigations Run")
def mitigations_run():
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
        return mitigations_run()

    network.application_characteristics = choose_application(
        network.model.to_directed(),
        1,
        score_characteristic_name,
        protected_characteristic_name,
    )

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
    ]

    protected_characteristic = network.characteristics[protected_characteristic_name]
    bias_by_recruiter = simulate(applicants, recruiters, protected_characteristic)

    db_run_id = save_run_to_db(
        engine,
        network,
        applicants,
        protected_characteristic_name,
        5,
        datetime.now() - start_time,
    )
    for bias, recruiter_bias_analysis in bias_by_recruiter.items():
        save_recruiter_run_to_db(engine, db_run_id, recruiter_bias_analysis)


if __name__ == "__main__":
    while True:
        try:
            mitigations_run()
        except Exception:
            pass
