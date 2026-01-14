import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "40_1_data.csv")

df = pd.read_csv(csv_file_path)

sns.set_palette("viridis")
sns.scatterplot(data=df, x="x", y="y", hue="color", legend=False, s=50)
plt.show()
