import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, '40_1_data.csv')

df = pd.read_csv(csv_file_path)

colors = ['#747FE3', '#8EE35D', '#E37346']
import pandas
import numpy
if isinstance(df, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(df.info())
    print("***")
    print(df.head(3))
    print("----***----")

elif isinstance(df, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(df.dtype)+" shape-"+str(df.shape))
    slices = tuple(slice(0, 3) for _ in range(df.ndim))
    print("***")
    print(df[slices])
    print("----***----")

elif isinstance(df, list):
    print("----***----")
    print("list")
    print("length-"+str(len(df)))
    print("***")
    print(df[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(df).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")
sns.scatterplot(data=df, x='x', y='y', hue='color', legend=False, palette=colors, s=50)
plt.show()
