import unittest
from main import Graph


class TestGraph(unittest.TestCase):
    def test_kruskal_1(self):
        g = Graph()
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 7)
        g.add_edge(1, 2, 5)
        g.add_edge(1, 3, 4)
        g.add_edge(1, 4, 3)
        g.add_edge(2, 4, 6)
        g.add_edge(4, 3, 2)
        self.assertEqual(g.kruskal_spanning_tree(), [[0, 1, 1], [4, 3, 2], [1, 4, 3], [1, 2, 5]])

    def test_kruskal_2(self):
        g = Graph()
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 4)
        g.add_edge(0, 3, 3)
        g.add_edge(1, 3, 2)
        g.add_edge(3, 3, 5)
        self.assertEqual(g.kruskal_spanning_tree(), [[0, 1, 1], [1, 3, 2], [0, 2, 4]])


if __name__ == '__main__':
    unittest.main()
