import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns

df = pd.DataFrame({
    'from': ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'E', 'F', 'G', 'H'],
    'to':   ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    })

G = nx.Graph()
G.add_edges_from(df.values)

groups_df = pd.DataFrame(index=G.nodes(), columns=['group'])

for node in G.nodes():
    if node in ['A', 'B', 'C', 'D']:
        group = 0
    elif node in ['E', 'F', 'G']:
        group = 1
    else:
        group = 2

    groups_df.loc[node, 'group'] = group

groups_df['group'] = groups_df['group'].astype(int)

fig, ax = plt.subplots(ncols=2)
cmap = ListedColormap(plt.cm.Dark2(np.arange(3)))

nx.draw(G, with_labels=True, node_color=groups_df['group'], cmap=cmap, ax=ax[0])
ax[0].set_title("Graph with Node Groups")

sns.countplot(data=groups_df.reset_index(), x='group', hue='group', palette=cmap.colors.tolist(), ax=ax[1], saturation=1)
ax[1].set_title("Count of Nodes per Group")
ax[1].set_xlabel("Group")
ax[1].set_ylabel("Count")

plt.show()
import pandas
import numpy
if isinstance(cmap.colors, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(cmap.colors.info())
    print("***")
    print(cmap.colors.head(3))
    print("----***----")

elif isinstance(cmap.colors, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(cmap.colors.dtype)+" shape-"+str(cmap.colors.shape))
    slices = tuple(slice(0, 3) for _ in range(cmap.colors.ndim))
    print("***")
    print(cmap.colors[slices])
    print("----***----")

elif isinstance(cmap.colors, list):
    print("----***----")
    print("list")
    print("length-"+str(len(cmap.colors)))
    print("***")
    print(cmap.colors[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(cmap.colors).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")
