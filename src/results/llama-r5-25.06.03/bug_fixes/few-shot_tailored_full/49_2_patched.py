import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

viz_dict = {"grid.linewidth": 4, "grid.color": "red"}
plt.rcParams.update(viz_dict)

fig, ax = plt.subplots(1, 1)
x = np.linspace(0, 14, 100)
sns.scatterplot(x=x, y=np.sin(x + 0.5) * 2)
ax.set_xlabel("Time")
ax.set_ylabel("Count")
plt.show()
