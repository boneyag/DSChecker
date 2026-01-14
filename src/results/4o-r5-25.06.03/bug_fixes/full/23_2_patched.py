import seaborn as sns

tips = sns.load_dataset("tips")

# Select a subset of numerical data from the DataFrame
numerical_data = tips[["total_bill", "tip", "size"]]
g = sns.heatmap(
    numerical_data, square=True, cbar_kws={"fraction": 0.01}, cmap="OrRd", linewidth=1
)
