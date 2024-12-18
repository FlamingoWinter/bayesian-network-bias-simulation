import networkx as nx
import matplotlib.pyplot as plt

from pgmpy.utils import get_example_model
model = get_example_model("sachs")

nx.draw(model)
plt.draw()