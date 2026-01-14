import seaborn as sns

tips = sns.load_dataset("tips")

correlation_matrix = tips.corr()
g = sns.heatmap(
    correlation_matrix,
    square=True,
    cbar_kws={"fraction": 0.01},
    cmap="OrRd",
    linewidth=1,
)
