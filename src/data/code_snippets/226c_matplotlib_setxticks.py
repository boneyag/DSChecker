import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.DataFrame(
    {
      'x': np.arange(10),
      'y': np.arange(10)
    }
)

fig, ax = plt.subplots()
ax.scatter(df['x'], df['y'])
ax.set_xticks(df['x'])
ax.set_xticklabels(df['x'])
plt.show()
