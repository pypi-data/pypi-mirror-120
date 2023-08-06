import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


output_plot = '/Users/songweizhi/Desktop/a.png'


num_list_1 = [1,2,3,4,5,6,7,5,6,7,4,5,6,7,6,6,6,7,5,3,4,7,4,3,4,5,4,3]
num_list_2 = [7,5,6,7,8,6,7,8,6,7,8,5,7,5,6,8]



data = [num_list_1, num_list_2]
box_plot = plt.boxplot(data, patch_artist=True, whiskerprops=dict(color='grey', linewidth=1), capprops=dict(color='grey'))

# set the color pf box
for box in box_plot['boxes']:
    box.set(linewidth=0)
    box.set_facecolor('lightblue')
    box.set_alpha(0.7)
    box.set_zorder(1)

# add dots, https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html
plt.plot(np.random.normal(1, 0.02, len(num_list_1)), num_list_1, '.', alpha=0.8, marker='o', color='orange', markersize=5, markeredgewidth=0, zorder=2)
plt.plot(np.random.normal(2, 0.02, len(num_list_2)), num_list_2, '.', alpha=0.8, marker='o', color='orange', markersize=5, markeredgewidth=0, zorder=2)

for i in [1,2]:
    y = data[i-1]
    x = np.random.normal(i, 0.02, len(y))
    plt.plot(x, y, 'r.', alpha=0.2)
plt.savefig(output_plot, dpi=300)
plt.close()


