import pymc as pm

class BayesianNetwork:
    def __init__(self, pm_model: pm.model.core.Model):
        self.model = pm_model
