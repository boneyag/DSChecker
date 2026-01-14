import seaborn as sns

tips = sns.load_dataset("tips")

g = sns.heatmap(
    tips.pivot_table(values="tip", index="day", columns="sex"),
    square=True,
    cbar_kws={"fraction": 0.01},
    cmap="OrRd",
    linewidth=1,
)
