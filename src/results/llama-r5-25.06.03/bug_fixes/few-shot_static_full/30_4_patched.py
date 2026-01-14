import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(100)

df = pd.DataFrame(
    {
        "A": ["spam", "eggs", "spam", "eggs"] * 3,
        "B": ["alpha", "beta", "gamma", "delta"] * 3,
        "C": [
            np.random.choice(
                pd.date_range(
                    datetime.datetime(2013, 1, 1), datetime.datetime(2013, 1, 12)
                )
            )
            for i in range(12)
        ],
        "D": np.random.randn(12),
        "E": np.random.randint(0, 4, 12),
    }
)

fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(df["C"], df["E"])

import matplotlib.dates as mdates

date = datetime.datetime(2013, 1, 5)
plt.text(mdates.date2num([date])[0], 0.5, "SAMPLE")
