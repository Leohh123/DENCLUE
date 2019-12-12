import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class Renderer(object):
    def __init__(self, x, y, cnt, bel):
        self.x = x
        self.y = y
        self.cnt = cnt
        self.bel = bel
        self.n = len(self.bel)
        plt.xlabel("x")
        plt.ylabel("y")

    def scatter(self):
        plt.scatter(self.x, self.y, c=[
            ("C" + str(self.bel[i])) if self.bel[i] != -1 else "0.5" for i in range(self.n)])

    def render(self, path="cluster_fig.png"):
        self.scatter()
        plt.savefig(path)
        plt.show()
