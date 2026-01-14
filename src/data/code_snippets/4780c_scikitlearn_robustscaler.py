from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split

import numpy as np

X = np.array([10000, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 20, 25]).reshape(-1, 1)
X_train, X_test = train_test_split(X, test_size=0.2, random_state=0)

rb_scaler = RobustScaler()
X_train_scaled = rb_scaler.fit_transform(X_train)
X_test_scaled = rb_scaler.transform(X_test)
