import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sbn
from matplotlib.dates import DateFormatter, MonthLocator

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "6_data.csv")

df = pd.read_csv(csv_file_path, header=0)

df["date"] = pd.to_datetime(df["date"])

fig, ax = plt.subplots()
ax = sbn.scatterplot(data=df, x="date", y="total", hue="location", style="type")
ax.legend(framealpha=0.5)
ax.xaxis.set_major_locator(MonthLocator())
ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
plt.show()
