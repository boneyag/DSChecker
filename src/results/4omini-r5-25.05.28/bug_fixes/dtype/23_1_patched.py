import seaborn as sns

tips = sns.load_dataset("tips")

g = sns.heatmap(
    tips.pivot_table(index="day", columns="sex", values="tip", aggfunc="mean"),
    square=True,
    cbar_kws={"fraction": 0.01},
    cmap="OrRd",
    linewidth=1,
)
