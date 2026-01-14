import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, '40_1_data.csv')

df = pd.read_csv(csv_file_path)

colors = ['#747FE3', '#8EE35D', '#E37346']
sns.set_palette(sns.color_palette(colors))
sns.scatterplot(data=df, x='x', y='y', hue='color', legend=False, s=50)
plt.show()
