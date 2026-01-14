from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, '34_1_data.csv')

df = pd.read_csv(csv_file_path, header=0)

impt = SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=0.0001)

imp_array = impt.fit_transform(df)

print(imp_array[:, 1])
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
