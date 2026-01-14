import numpy as np

arr = np.ones((3, 4))
import pandas
import numpy
if isinstance(arr, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(arr.info())
    print("***")
    print(arr.head(3))
    print("----***----")

elif isinstance(arr, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(arr.dtype)+" shape-"+str(arr.shape))
    slices = tuple(slice(0, 3) for _ in range(arr.ndim))
    print("***")
    print(arr[slices])
    print("----***----")

elif isinstance(arr, list):
    print("----***----")
    print("list")
    print("length-"+str(len(arr)))
    print("***")
    print(arr[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(arr).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")

arr = np.insert(arr, 1, 3, axis=1)
