from typing import List, Dict

import pymc as pm


class BayesianNetwork:
    def __init__(self, pm_model: pm.Model, score_characteristic: str = "score",
                 application_characteristics: List[str] = None,
                 categories_by_categorical_variable=None):
        if application_characteristics is None:
            application_characteristics = []

        if categories_by_categorical_variable is None:
            categories_by_categorical_variable = []

        self.model = pm_model
        self.categories_by_categorical_variable: Dict[str, List[str]] = categories_by_categorical_variable
        self.score_characteristic: str = score_characteristic
        self.application_characteristics: List[str] = application_characteristics
