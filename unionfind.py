class UnionFind(object):
    def __init__(self, n):
        self.n = n
        self.par = [i for i in range(self.n)]
        self.count = self.n
        self.sid = []
        self.pos = []

    def find(self, x):
        r = x
        while self.par[r] != r:
            r = self.par[r]
        while x != r:
            t = self.par[x]
            self.par[x] = r
            x = t
        return r

    def merge(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.par[px] = py
            self.count -= 1

    def is_same(self, x, y):
        return self.find(x) == self.find(y)

    def arrange(self):
        no = [-1 for i in range(self.n)]
        cnt = 0
        for i in range(self.n):
            p = self.find(i)
            if no[p] == -1:
                no[p] = cnt
                self.pos.append(p)
                cnt += 1
            self.sid.append(no[p])


if __name__ == "__main__":
    n = int(input())
    uf = UnionFind(n)
    while True:
        x, y = list(map(int, input().split()))
        if x == -1:
            break
        uf.merge(x, y)
        print([uf.find(i) for i in range(n)])
    uf.arrange()
    print("sid", uf.sid)
    print("pos", uf.pos)
