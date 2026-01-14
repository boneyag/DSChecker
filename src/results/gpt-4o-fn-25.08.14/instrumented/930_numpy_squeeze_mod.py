import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

np.random.seed(0)

X = pd.DataFrame({'x': np.random.randn(10)})
y = np.random.randn(10).reshape(-1, 1)

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_tr, y_tr)
preds = model.predict(np.squeeze(X_te.values))
import pandas
import numpy
if isinstance(X_te, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(X_te.info())
    print("***")
    print(X_te.head(3))
    print("----***----")

elif isinstance(X_te, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(X_te.dtype)+" shape-"+str(X_te.shape))
    slices = tuple(slice(0, 3) for _ in range(X_te.ndim))
    print("***")
    print(X_te[slices])
    print("----***----")

elif isinstance(X_te, list):
    print("----***----")
    print("list")
    print("length-"+str(len(X_te)))
    print("***")
    print(X_te[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(X_te).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")
