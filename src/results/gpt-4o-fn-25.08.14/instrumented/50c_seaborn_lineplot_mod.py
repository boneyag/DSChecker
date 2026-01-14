import pandas as pd
import numpy as np
import seaborn as sb

data = {
    'X': list(np.arange(0, 10, 1)),
    'Y': [1, 3, 2, 5, 7, 8, 8, 9, 10, 12]
    }
df = pd.DataFrame(data)
df2 = pd.DataFrame(np.ones(10), columns=['ones'])
df_new = pd.concat([df2, df], axis=1)

X = df_new.loc[:, ['ones', 'X']].values
Y = df_new['Y'].values.reshape(-1, 1)

theta = np.array([0.5, 0.2]).reshape(-1, 1)

Y_pred = X.dot(theta)
import pandas
import numpy
if isinstance(Y_pred, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(Y_pred.info())
    print("***")
    print(Y_pred.head(3))
    print("----***----")

elif isinstance(Y_pred, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(Y_pred.dtype)+" shape-"+str(Y_pred.shape))
    slices = tuple(slice(0, 3) for _ in range(Y_pred.ndim))
    print("***")
    print(Y_pred[slices])
    print("----***----")

elif isinstance(Y_pred, list):
    print("----***----")
    print("list")
    print("length-"+str(len(Y_pred)))
    print("***")
    print(Y_pred[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(Y_pred).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")

sb.lineplot(data=None, x=df['X'].values, y=Y_pred.reshape(-1))
