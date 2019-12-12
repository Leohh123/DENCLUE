import numpy as np
import math
from unionfind import UnionFind

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


H = 0.5  # Smoothing parameter
K = 0.5  # Linkage distance
DELTA = 0.2  # Speed of convergence
XI = 0.01  # Denoising parameter
MAX_TIMES = 50


def sqrs(x):
    return (x ** 2).sum()


def slen(x):
    return sqrs(x) ** 0.5


def dist(x, y):
    return sqrs(x - y) ** 0.5


def k_gauss(x):
    return math.exp(-0.5 * sqrs(x)) / (2 * math.pi)


def get_z(x, y, f):
    m, n = x.shape
    z = np.empty((m, n))
    for i in range(m):
        for j in range(n):
            z[i, j] = f(x[i, j], y[i, j])
    return z


class Denclue2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.n = len(x)
        assert(self.n == len(y))
        self.ps = [np.array([self.x[i], self.y[i]]) for i in range(self.n)]
        self.attrs = []
        self.bel = []
        self.is_out = []
        self.cluster_id = []

    def render_dens_fig(self, path="./dens_fig.png"):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        EPN = 50
        X = np.linspace(0, 10, EPN)
        Y = np.linspace(0, 10, EPN)
        X, Y = np.meshgrid(X, Y)
        Z = get_z(X, Y, lambda x, y: self.f_gauss(np.array([x, y])))
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
        plt.savefig(path)
        plt.show()

    def f_gauss(self, x):
        s = 0
        for p in self.ps:
            s += k_gauss((x - p) / H)
        return s / (self.n * (H ** 2))

    def delta_f(self, x):
        s = np.array([0., 0.])
        for p in self.ps:
            s += k_gauss((x - p) / H) * (p - x)
        return s / ((H ** 4) * self.n)

    def next_pos(self, x):
        d = self.delta_f(x)
        return x + d * DELTA / slen(d)

    def get_max(self, start):
        x = start
        for i in range(MAX_TIMES):
            y = self.next_pos(x)
            if self.f_gauss(y) < self.f_gauss(x):
                break
            x = y
        return x

    def climbs(self):
        for i in range(self.n):
            print("clms", i, self.ps[i])
            mx = self.get_max(self.ps[i])
            self.attrs.append(mx)

    def merge_same(self):
        uf = UnionFind(self.n)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if dist(self.attrs[i], self.attrs[j]) < 2 * DELTA:
                    uf.merge(i, j)
        uf.arrange()
        new_attrs = []
        for position in uf.pos:
            new_attrs.append(self.attrs[position])
        self.attrs = new_attrs
        for i in range(self.n):
            self.bel.append(uf.sid[i])

    def tag_outs(self):
        for at in self.attrs:
            dens = self.f_gauss(at)
            self.is_out.append(dens < XI)

    def merge_cluster(self):
        uf = UnionFind(len(self.attrs))
        is_higher = [self.f_gauss(p) >= XI for p in self.ps]
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.bel[i] != self.bel[j] \
                        and is_higher[i] \
                        and is_higher[j] \
                        and (not self.is_out[self.bel[i]]) \
                        and (not self.is_out[self.bel[j]]) \
                        and dist(self.ps[i], self.ps[j]) < K:
                    uf.merge(self.bel[i], self.bel[j])
        uf.arrange()
        for i in range(len(self.attrs)):
            self.cluster_id.append(uf.sid[i])

    def get_result(self):
        res = []
        for i in range(self.n):
            if self.is_out[self.bel[i]]:
                res.append(-1)
            else:
                res.append(self.cluster_id[self.bel[i]])
        no = [-1 for i in range(len(self.attrs))]
        cnt = 0
        for i in range(len(res)):
            if res[i] != -1:
                if no[res[i]] == -1:
                    no[res[i]] = cnt
                    cnt += 1
                res[i] = no[res[i]]
        return cnt, res

    def work(self):
        print("climbs")
        self.climbs()
        print("merge_same")
        self.merge_same()
        print("tag_outs")
        self.tag_outs()
        print("merge_cluster")
        self.merge_cluster()


if __name__ == "__main__":
    x = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 4, 4])
    y = np.array([0, 1, 3, 5, 6, 0, 1, 3, 5, 6, 1, 3])
    dc = Denclue2D(x, y)
    dc.work()
    print(dc.get_result())
