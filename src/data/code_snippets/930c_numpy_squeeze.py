import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

np.random.seed(0)

X = pd.DataFrame({'x': np.random.randn(10)})
y = np.random.randn(10)

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_tr, y_tr)
preds = model.predict(X_te)
