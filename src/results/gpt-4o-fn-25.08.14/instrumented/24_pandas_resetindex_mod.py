import pandas as pd

df = pd.DataFrame({
    'x1': [1, 2, 2, 1, 1, 4, 4, 4],
    'x2': [2, 2, 2, 1, 1, 4, 1, 4],
    'y': ['a', 'a', 'b', 'a', 'a', 'b', 'b', 'a']
})

df['z'] = df.groupby(['y']).apply(lambda x: (x['x1'] != x['x1'].shift(-1)) | (x['x2'] != x['x2'].shift(-1)))
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
    print("----***----")
    print("Unsuported type for instrumentation")
    print("----***----")
