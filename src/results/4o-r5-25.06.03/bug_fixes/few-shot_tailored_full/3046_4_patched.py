import matplotlib.pyplot as plt


def get_active_figure():
    return plt.gcf()


fig, ax = plt.subplots()
ax.plot([0, 1, 2, 3], [0, 4, 5, 6])
plt.show(block=False)
