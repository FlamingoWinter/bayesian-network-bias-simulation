from typing import List, Dict

import pymc as pm


class BayesianNetwork:
    def __init__(self, pm_model: pm.Model, score_characteristic: str = "score",
                 application_characteristics: List[str] = None,
                 categories_by_categorical_variable=None,
                 description_by_characteristic: Dict[str, str] = None,
                 description: str = ""):
        if application_characteristics is None:
            application_characteristics = []

        if categories_by_categorical_variable is None:
            categories_by_categorical_variable = {}

        if description_by_characteristic is None:
            description_by_characteristic = {}

        self.model = pm_model
        self.categories_by_categorical_variable: Dict[str, List[str]] = categories_by_categorical_variable
        self.score_characteristic: str = score_characteristic
        self.application_characteristics: List[str] = application_characteristics
        self.descriptions_by_characteristic: Dict[str, str] = description_by_characteristic
        self.description = description

    def set_description_for_characteristic(self, characteristic: str, description: str):
        self.descriptions_by_characteristic[characteristic] = description

    def set_description(self, description: str):
        self.description = description
