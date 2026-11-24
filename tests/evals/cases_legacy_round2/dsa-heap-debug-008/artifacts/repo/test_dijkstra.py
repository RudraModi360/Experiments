import unittest
from dijkstra import shortest_paths
class DijkstraTest(unittest.TestCase):
    def test_basic(self):
        g = {"a":[("b",1),("c",4)],"b":[("c",2)],"c":[]}
        self.assertEqual(shortest_paths(g,"a"), {"a":0,"b":1,"c":3})
    def test_disconnected(self):
        g = {"a":[("b",1)],"c":[]}
        self.assertEqual(shortest_paths(g,"a"), {"a":0,"b":1})
    def test_tie(self):
        g = {"a":[("b",1),("c",1)],"b":[("d",1)],"c":[("d",1)],"d":[]}
        self.assertEqual(shortest_paths(g,"a")["d"], 2)
