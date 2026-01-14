from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3, 4, 5],
    'b': ['a', 'b', 'a', 'a', 'b'],
    'c': [1, 0, 1, 1, 1]
})
X = df.drop(columns="c")
y = df.c

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preprocessor = ColumnTransformer([
    ('numeric', MinMaxScaler(), ['a']),
    ('categoric', OneHotEncoder(), ["b"]),
])

pipeline = Pipeline([
    ('prep', preprocessor),
    ('algo', GaussianNB)
])

cls = pipeline.fit(X_train, y_train)
