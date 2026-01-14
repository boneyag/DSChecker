import numpy as np

x = np.array([[-1, 2, 3], [-4, -2, 8]], dtype=np.float32)

initial_value = None
where_value = None

if initial_value is not None and where_value is not None:
    res = np.amin(a=x, axis=1, keepdims=False, initial=initial_value, where=where_value, out=None)
else:
    res = np.amin(a=x, axis=1, keepdims=False, out=None)
print(res)
import pandas
import numpy
if isinstance(where_value, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(where_value.info())
    print("***")
    print(where_value.head(3))
    print("----***----")

elif isinstance(where_value, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(where_value.dtype)+" shape-"+str(where_value.shape))
    slices = tuple(slice(0, 3) for _ in range(where_value.ndim))
    print("***")
    print(where_value[slices])
    print("----***----")

elif isinstance(where_value, list):
    print("----***----")
    print("list")
    print("length-"+str(len(where_value)))
    print("***")
    print(where_value[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(where_value).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")
