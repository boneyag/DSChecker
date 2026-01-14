import matplotlib.pyplot as plt


def get_active_figure():
    return plt.gcf()


fig, ax = plt.subplots()
ax.plot([0, 1, 2, 3], [0, 4, 5, 6])

ac_fig = get_active_figure()

if ac_fig is None:
    print("No active figure")
else:
    ax.text(0.4, 0.4, "Add a label to the current active figure")
    plt.show(block=False)
    plt.close()
