import seaborn as sns

tips = sns.load_dataset("tips")
pivot_table = tips.pivot_table(
    index="day", columns="time", values="total_bill", aggfunc="mean"
)
g = sns.heatmap(
    pivot_table, square=True, cbar_kws={"fraction": 0.01}, cmap="OrRd", linewidth=1
)
