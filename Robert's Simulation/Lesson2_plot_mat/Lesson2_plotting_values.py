import numpy as np, matplotlib as mpl, matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D


def get_matrix_from_file(text_file : str):
    # from os import chdir
    # chdir('../')
    asc_matrix = np.loadtxt(text_file , skiprows=3)
    return asc_matrix

def plot_matrix():
    return

# Jumping Jesus on a pogo stick python does not simulate 47k datapoints very well, on a 3d plane
matrix = get_matrix_from_file("YSFIL.ASC")
pE= matrix[:,1]
pF= matrix[:,2]
pG= matrix[:,3]


# USE PLOT, IT IS A 3D LINE GRAPH. ANIMATION IS MUCH SMOOTHER OVER SCATTER PLOT
fig = plot.figure(figsize=(7,7))
ax = fig.add_subplot(111,projection = '3d')

ax.plot(pE,pF,pG, c='r', marker = 'o')
ax.set_xlabel('pE Label')
ax.set_ylabel('pF Label')
ax.set_zlabel('pG Label')
plot.show()
