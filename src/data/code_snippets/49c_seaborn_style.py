import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

scale_dict = {
    'grid.linewidth': 4
}
sns.set_context(rc=scale_dict)

style_dict = {
    'axes.grid': True,
    'grid.color': 'red'
}
sns.set_style(rc=style_dict)

fig, ax = plt.subplots(1, 1)
x = np.linspace(0, 14, 100)
sns.scatterplot(x=x, y=np.sin(x + .5) * 2)
ax.set_xlabel("Time")
ax.set_ylabel("Count")
plt.show()
