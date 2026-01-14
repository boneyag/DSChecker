import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "40_1_data.csv")

df = pd.read_csv(csv_file_path)

colors = ["#747FE3", "#8EE35D", "#E37346"]
sns.set_palette(sns.color_palette(colors))
df["color"] = df["color"].astype("category")
plt.show()
