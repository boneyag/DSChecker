import pandas as pd

df = pd.DataFrame({
    'l1': [1, 2, 3, 4, 5, 6, 7],
    'l2': ['a. 12', 'b. 75', '23', 'sc/a 34', '85', 'a 32', 'b 345']
})

df['l2'].replace(to_replace=r'^\d+$', value=0, regex=True)
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
