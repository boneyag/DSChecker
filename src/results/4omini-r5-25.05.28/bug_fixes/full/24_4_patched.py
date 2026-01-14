import pandas as pd

df = pd.DataFrame(
    {
        "x1": [1, 2, 2, 1, 1, 4, 4, 4],
        "x2": [2, 2, 2, 1, 1, 4, 1, 4],
        "y": ["a", "a", "b", "a", "a", "b", "b", "a"],
    }
)

df["z"] = df.groupby(["y"]).apply(
    lambda x: (x["x1"] != x["x1"].shift(-1)).fillna(False)
    | (x["x2"] != x["x2"].shift(-1)).fillna(False)
)
