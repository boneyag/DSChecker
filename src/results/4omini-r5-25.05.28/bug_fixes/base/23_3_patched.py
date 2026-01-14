import seaborn as sns

tips = sns.load_dataset("tips")

pivot_tips = tips.pivot_table(
    index="day", columns="time", values="total_bill", aggfunc="mean"
)
