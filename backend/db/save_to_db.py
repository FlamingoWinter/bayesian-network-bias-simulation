import json
import os
from datetime import timedelta

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import Engine, text
from sqlalchemy import create_engine

from backend.bias.recruiter_bias_analysis import RecruiterBiasAnalysis
from backend.candidates.candidate_group import CandidateGroup
from backend.entropy.entropy import categorical_entropy_of_array
from backend.network.pgmpy_network import PgmPyNetwork


def get_engine() -> Engine:
    load_dotenv()

    return create_engine(
        f'postgresql://postgres:{os.getenv("DB_PASSWORD")}@db.wsfskureutearqgkfdeq.supabase.co:5432/postgres')


def save_run_to_db(engine: Engine,
                   network: PgmPyNetwork, candidate_group: CandidateGroup,
                   protected_characteristic_name: str, condition: int, run_duration: timedelta) -> int:
    graph = json.dumps(network.to_network_response())

    protected = candidate_group.characteristics[protected_characteristic_name]
    score = candidate_group.characteristics[network.score_characteristic]

    proportion_competent = score.sum() / len(score)
    proportion_group_1 = 1 - (protected.sum() / len(score))
    proportion_competent_group_1 = ((score == 1) & (protected == 0)).sum() / (protected == 0).sum()
    proportion_competent_group_2 = ((score == 1) & (protected == 1)).sum() / (protected == 1).sum()

    protected_score_mut_inf = (
            categorical_entropy_of_array(protected)
            + categorical_entropy_of_array(score)
            - categorical_entropy_of_array(np.column_stack((protected, score))))

    data = pd.DataFrame([{
        "condition": condition,
        "graph": graph,
        "competent_rate": proportion_competent,
        "proportion_group_1": proportion_group_1,
        "competent_rate_group_1": proportion_competent_group_1,
        "competent_rate_group_2": proportion_competent_group_2,
        "protected_score_mut_inf": protected_score_mut_inf,
        "protected_characteristic": protected_characteristic_name,
        "application_characteristics": network.application_characteristics,
        "score_characteristic": network.score_characteristic,
        "date": pd.Timestamp.now(tz='UTC'),
        "run_duration": run_duration,
    }])

    with engine.connect() as conn:
        columns = ", ".join(data.columns)
        placeholders = ", ".join([f":{col}" for col in data.columns])
        result = conn.execute(
            text(f"INSERT INTO runs ({columns}) VALUES ({placeholders}) RETURNING id"),
            data.to_dict(orient="records")
        )
        conn.commit()
        inserted_ids = [row[0] for row in result]

    print("Inserted IDs:", inserted_ids)

    return inserted_ids[0]


def save_recruiter_run_to_db(engine: Engine,
                             db_run_id: int, recruiter_bias_analysis: RecruiterBiasAnalysis) -> str:
    for mitigation_name, mitigation_bias_analysis in recruiter_bias_analysis.analysis_by_mitigation.items():
        data = pd.DataFrame([{
            "run_id": db_run_id,
            "recruiter": recruiter_bias_analysis.recruiter.name,
            "mitigation": mitigation_name,
            "accuracy": mitigation_bias_analysis.general.accuracy,
            "hired_rate": mitigation_bias_analysis.general.hired_rate,
            "hired_rate_group_1": mitigation_bias_analysis.by_group["1"].hired_rate,
            "hired_rate_group_2": mitigation_bias_analysis.by_group["2"].hired_rate,
            "fpr": mitigation_bias_analysis.general.false_positive_rate,
            "fpr_group_1": mitigation_bias_analysis.by_group["1"].false_positive_rate,
            "fpr_group_2": mitigation_bias_analysis.by_group["2"].false_positive_rate,
            "fnr": mitigation_bias_analysis.general.false_negative_rate,
            "fnr_group_1": mitigation_bias_analysis.by_group["1"].false_negative_rate,
            "fnr_group_2": mitigation_bias_analysis.by_group["2"].false_negative_rate,
            "f_o_r": mitigation_bias_analysis.general.false_omission_rate,
            "f_o_r_group_1": mitigation_bias_analysis.by_group["1"].false_omission_rate,
            "f_o_r_group_2": mitigation_bias_analysis.by_group["2"].false_omission_rate,
            "fdr": mitigation_bias_analysis.general.false_discovery_rate,
            "fdr_group_1": mitigation_bias_analysis.by_group["1"].false_discovery_rate,
            "fdr_group_2": mitigation_bias_analysis.by_group["2"].false_discovery_rate,
        }])

        with engine.connect() as conn:
            columns = ", ".join(data.columns)
            placeholders = ", ".join([f":{col}" for col in data.columns])
            result = conn.execute(
                text(f"INSERT INTO recruiter_runs ({columns}) VALUES ({placeholders}) RETURNING id"),
                data.to_dict(orient="records")
            )
            conn.commit()
            inserted_ids = [row[0] for row in result]

        print("Inserted IDs:", inserted_ids)

    return ""
