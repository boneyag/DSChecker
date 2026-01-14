import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

np.random.seed(0)

X = pd.DataFrame({'x': np.random.randn(10)})
y = np.random.randn(10)
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

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_tr, y_tr)
preds = model.predict(X_te)
