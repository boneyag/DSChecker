import matplotlib.pyplot as plt
import seaborn as sbn

tips = sbn.load_dataset("tips")

fig, ax = plt.subplots(figsize=(5, 6))
sbn.scatterplot(data=tips, x="total_bill", y="tip", hue="sex", ax=ax)
# ax.legend()  # This line can be removed or commented out
plt.show()
