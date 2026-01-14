import numpy as np
import pandas as pd
import seaborn as sb

data = {"X": list(np.arange(0, 10, 1)), "Y": [1, 3, 2, 5, 7, 8, 8, 9, 10, 12]}
df = pd.DataFrame(data)
df2 = pd.DataFrame(np.ones(10), columns=["ones"])
df_new = pd.concat([df2, df], axis=1)

X = df_new.loc[:, ["ones", "X"]].values
Y = df_new["Y"].values.reshape(-1, 1)

theta = np.array([0.5, 0.2]).reshape(-1, 1)

Y_pred = X.dot(theta)

sb.lineplot(x=df["X"].values, y=Y_pred.flatten())
