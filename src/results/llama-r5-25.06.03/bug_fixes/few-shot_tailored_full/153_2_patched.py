import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

df = pd.DataFrame(
    {
        "x": [74, 74, 74, 74, 74, 74, 74, 74, 192, 74],
        "y": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "z": np.zeros(10),
        "dx": np.ones(10) * 10,
        "dy": np.ones(10),
        "dz": [1455, 1219, 1240, 1338, 1276, 1298, 1292, 1157, 486, 1388],
    }
)

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.bar3d(df["x"], df["y"], df["z"], df["dx"], df["dy"], df["dz"], color="b")

plt.show()
