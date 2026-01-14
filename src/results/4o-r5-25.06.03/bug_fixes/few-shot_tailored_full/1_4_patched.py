import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

X = pd.DataFrame(
    {
        "city": ["London", "London", "Paris", "NewYork"],
        "country": ["UK", "0.2", "FR", "US"],
        "expert_rating": [5, 3, 4, 5],
        "user_rating": [4, 5, 4, 3],
    }
)

categorical_features = ["city", "country"]
one_hot = OneHotEncoder()
transformer = ColumnTransformer(
    [("one_hot", one_hot, categorical_features)], remainder="passthrough"
)
transformed_X = transformer.fit_transform(X)
