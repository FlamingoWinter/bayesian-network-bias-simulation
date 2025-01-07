import pymc as pm


def visualise_model_as_network(model: pm.Model):
    pm.model_to_graphviz(model).render("asia", format="png", view=True, cleanup=True)
