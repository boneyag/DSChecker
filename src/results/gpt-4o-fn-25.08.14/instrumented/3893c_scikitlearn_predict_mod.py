from sklearn.dummy import DummyClassifier
import numpy as np

X = [[0], [0], [0], [0], [0]]
y = [1, 2, 1, 1, 2]

clf = DummyClassifier(strategy="most_frequent", random_state=0)
import pandas
import numpy
if isinstance(y, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(y.info())
    print("***")
    print(y.head(3))
    print("----***----")

elif isinstance(y, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(y.dtype)+" shape-"+str(y.shape))
    slices = tuple(slice(0, 3) for _ in range(y.ndim))
    print("***")
    print(y[slices])
    print("----***----")

elif isinstance(y, list):
    print("----***----")
    print("list")
    print("length-"+str(len(y)))
    print("***")
    print(y[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(y).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")
clf.fit(X, y)

predictions = clf.predict(X)
print(predictions == np.ones(len(y)))
