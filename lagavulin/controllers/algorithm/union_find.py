
class UnionFindTree(object):
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def unite(self, x, y):
        par_x = self.find(x)
        par_y = self.find(y)
        if par_x == par_y:
            return

        rank_x = self.rank[x]
        rank_y = self.rank[y]
        # 低い方の木に、高い方の木の根を結合する
        if rank_x < rank_y:
            # yの根にxの木を結合。
            self.parent[par_x] = par_y
        else:
            self.parent[par_y] = par_x
            if rank_x == rank_y:
                self.rank[x] += 1

    def find(self, x):
        while x != self.parent[x]:
            x = self.parent[x]
        return x

    def is_same(self, x, y):
        return self.find(x) == self.find(y)
