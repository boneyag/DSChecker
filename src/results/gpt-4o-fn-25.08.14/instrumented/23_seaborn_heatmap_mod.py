import seaborn as sns

tips = sns.load_dataset('tips')
import pandas
import numpy
if isinstance(tips, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(tips.info())
    print("***")
    print(tips.head(3))
    print("----***----")

elif isinstance(tips, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(tips.dtype)+" shape-"+str(tips.shape))
    slices = tuple(slice(0, 3) for _ in range(tips.ndim))
    print("***")
    print(tips[slices])
    print("----***----")

elif isinstance(tips, list):
    print("----***----")
    print("list")
    print("length-"+str(len(tips)))
    print("***")
    print(tips[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(tips).__name__}")
    print("----***----")
    print("Unsuported type for instrumentation")
    print("----***----")

g = sns.heatmap(tips, square=True, cbar_kws={'fraction': 0.01}, cmap='OrRd', linewidth=1)
