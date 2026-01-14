from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split

import numpy as np

X = np.array([10000, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 20, 25]).reshape(-1, 1)
X_train, X_test = train_test_split(X, test_size=0.2, random_state=0)

rb_scaler = RobustScaler()
X_train_scaled = rb_scaler.fit_transform(X_train)
X_test_scaled = rb_scaler.fit_transform(X_test)
import pandas
import numpy
if isinstance(X_test, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(X_test.info())
    print("***")
    print(X_test.head(3))
    print("----***----")

elif isinstance(X_test, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(X_test.dtype)+" shape-"+str(X_test.shape))
    slices = tuple(slice(0, 3) for _ in range(X_test.ndim))
    print("***")
    print(X_test[slices])
    print("----***----")

elif isinstance(X_test, list):
    print("----***----")
    print("list")
    print("length-"+str(len(X_test)))
    print("***")
    print(X_test[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(X_test).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")
