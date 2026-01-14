import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.DataFrame(
    {
        "age": [19, 18, 28, 33, 32],
        "sex": ["female", "male", "male", "male", "male"],
        "bmi": [27.900, 33.770, 33.000, 22.705, 28.880],
        "smoker": [
            "yes",
            "no",
            "no",
            "no",
            "no",
        ],
        "region": ["sw", "sw", "sw", "nw", "nw"],
        "charges": [16884, 1725, 4449, 21984, 3886],
    }
)


class HealthyAttributeAdder(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        healthy = (X["smoker"] == "no") & (X["bmi"].between(18.5, 24.9))
        new_X = X.copy()
        new_X["healthy"] = healthy.astype(int)
        return new_X


num_col = ["age", "bmi"]
cat_col = ["sex", "smoker", "region"]
y = df.pop("charges")
X = df
all_col = X.columns
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

transform_pipeline = ColumnTransformer(
    [
        ("ss", StandardScaler(), num_col),
        ("ohe", OneHotEncoder(), cat_col),
    ]
)

price_pipeline = Pipeline(
    [
        ("add_healthy", HealthyAttributeAdder()),
        ("transform", transform_pipeline),
        ("lasso", Lasso()),
    ]
)

price_pipeline.fit(X_train, y_train)
y_pred = price_pipeline.predict(X_test)
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.DataFrame(
    {
        "age": [19, 18, 28, 33, 32],
        "sex": ["female", "male", "male", "male", "male"],
        "bmi": [27.900, 33.770, 33.000, 22.705, 28.880],
        "smoker": [
            "yes",
            "no",
            "no",
            "no",
            "no",
        ],
        "region": ["sw", "sw", "sw", "nw", "nw"],
        "charges": [16884, 1725, 4449, 21984, 3886],
    }
)


class HealthyAttributeAdder(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        healthy = (X["smoker"] == "no") & (X["bmi"].between(18.5, 24.9))
        new_X = X.copy()
        new_X["healthy"] = healthy.astype(int)
        return new_X


num_col = ["age", "bmi"]
cat_col = ["sex", "smoker", "region", "healthy"]
y = df.pop("charges")
X = df
all_col = X.columns
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

num_col_plus_healthy = num_col + ["healthy"]
transform_pipeline = ColumnTransformer(
    [
        ("ss", StandardScaler(), num_col_plus_healthy),
    ]
)

price_pipeline = Pipeline(
    [
        ("add_healthy", HealthyAttributeAdder()),
        ("transform", transform_pipeline),
        ("lasso", Lasso()),
    ]
)

price_pipeline.fit(X_train, y_train)
y_pred = price_pipeline.predict(X_test)
