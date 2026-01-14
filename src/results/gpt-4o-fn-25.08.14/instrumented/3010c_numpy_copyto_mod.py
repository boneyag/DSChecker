import numpy as np

np.random.seed(42)

size = 1000000
a = np.random.rand(size)
cp = np.random.rand(size)
mask = np.random.randint(2, size=size, dtype=bool)
import pandas
import numpy
if isinstance(mask, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(mask.info())
    print("***")
    print(mask.head(3))
    print("----***----")

elif isinstance(mask, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(mask.dtype)+" shape-"+str(mask.shape))
    slices = tuple(slice(0, 3) for _ in range(mask.ndim))
    print("***")
    print(mask[slices])
    print("----***----")

elif isinstance(mask, list):
    print("----***----")
    print("list")
    print("length-"+str(len(mask)))
    print("***")
    print(mask[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(mask).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")

np.copyto(a, cp, where=mask)
