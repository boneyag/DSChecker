import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
np.random.seed(100)

df = pd.DataFrame({'A': ['spam', 'eggs', 'spam', 'eggs'] * 3,
                   'B': ['alpha', 'beta', 'gamma', 'delta'] * 3,
                   'C': [np.random.choice(pd.date_range(datetime.datetime(2013, 1, 1), datetime.datetime(2013, 1, 12))) for i in range(12)],
                   'D': np.random.randn(12),
                   'E': np.random.randint(0, 4, 12)})

fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(df['C'], df['E'])

plt.text(datetime.datetime.strptime("2013-01-05"), 0.5, "SAMPLE")
