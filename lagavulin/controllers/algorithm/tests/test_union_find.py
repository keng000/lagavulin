import unittest
from lagavulin.controllers.algorithm.union_find import UnionFindTree


class TestUnionFindTree(unittest.TestCase):
    def setUp(self):
        self.length = 8
        self.unif_tree = UnionFindTree(self.length)

    def test_init_is_same(self):
        for idx in range(self.length-1):
            self.assertFalse(self.unif_tree.is_same(idx, idx+1))

    def test_init_find(self):
        for idx in range(self.length - 1):
            self.assertEqual(self.unif_tree.find(idx), idx)

    def test_unite(self):
        # 単一ノードからなる木の結合
        self.unif_tree.unite(0, 1)
        self.assertTrue(self.unif_tree.is_same(0, 1))
        for idx in range(1, self.length - 1):
            self.assertFalse(self.unif_tree.is_same(idx, idx + 1))

        self.unif_tree.unite(2, 3)
        for idx in range(3, self.length - 1):
            self.assertFalse(self.unif_tree.is_same(idx, idx + 1))

        # 結合していない木が違う木に属していることを確認
        self.assertFalse(self.unif_tree.is_same(1, 2))

        # 高さのある木同士の結合
        self.unif_tree.unite(1, 2)
        self.assertTrue(self.unif_tree.is_same(0, 2))
        self.assertTrue(self.unif_tree.is_same(1, 2))
        self.assertTrue(self.unif_tree.is_same(0, 3))
        self.assertTrue(self.unif_tree.is_same(1, 3))

        self.assertEqual(self.unif_tree.find(0), self.unif_tree.find(3))


if __name__ == '__main__':
    unittest.main()
