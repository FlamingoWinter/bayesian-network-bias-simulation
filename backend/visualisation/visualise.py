import pymc as pm


def visualise_model_as_network(model: pm.Model):
    if model.name == "":
        model.name = "unnamed_network"
    pm.model_to_graphviz(model).render(model.name, format="png", view=True, cleanup=True)
