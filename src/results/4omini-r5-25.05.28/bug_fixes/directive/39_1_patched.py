import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import ListedColormap

df = pd.DataFrame(
    {
        "from": ["A", "A", "B", "B", "C", "C", "D", "E", "F", "G", "H"],
        "to": ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
    }
)

G = nx.Graph()
G.add_edges_from(df.values)

groups_df = pd.DataFrame(index=G.nodes(), columns=["group"])

for node in G.nodes():
    if node in ["A", "B", "C", "D"]:
        group = 0
    elif node in ["E", "F", "G"]:
        group = 1
    else:
        group = 2

    groups_df.loc[node, "group"] = group

groups_df["group"] = groups_df["group"].astype(int)
print(groups_df.info(), groups_df.head(3))
fig, ax = plt.subplots(ncols=2)
cmap = ListedColormap(plt.cm.Dark2(np.arange(3)))

nx.draw(G, with_labels=True, node_color=groups_df["group"], cmap=cmap, ax=ax[0])
ax[0].set_title("Graph with Node Groups")

sns.countplot(
    data=groups_df.reset_index(),
    x="group",
    hue="group",
    palette=cmap.colors.tolist(),
    ax=ax[1],
    saturation=1,
)
ax[1].set_title("Count of Nodes per Group")
ax[1].set_xlabel("Group")
ax[1].set_ylabel("Count")

plt.show()
