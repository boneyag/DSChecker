import seaborn as sns

tips = sns.load_dataset('tips')

tips_new = tips.drop(['sex', 'smoker', 'time','total_bill'], axis=1)
df_heatmap = tips_new.pivot_table("tip", "day", "size")

g = sns.heatmap(df_heatmap, square=True, cbar_kws={'fraction': 0.01}, cmap='OrRd', linewidth=1)
import pandas
import numpy
if isinstance(df_heatmap, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(df_heatmap.info())
    print("***")
    print(df_heatmap.head(3))
    print("----***----")

elif isinstance(df_heatmap, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(df_heatmap.dtype)+" shape-"+str(df_heatmap.shape))
    slices = tuple(slice(0, 3) for _ in range(df_heatmap.ndim))
    print("***")
    print(df_heatmap[slices])
    print("----***----")

elif isinstance(df_heatmap, list):
    print("----***----")
    print("list")
    print("length-"+str(len(df_heatmap)))
    print("***")
    print(df_heatmap[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(df_heatmap).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")
