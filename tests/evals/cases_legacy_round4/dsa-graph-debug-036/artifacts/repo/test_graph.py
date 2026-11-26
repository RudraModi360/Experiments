import unittest
from graph import bfs, dfs, dijkstra
class GraphTest(unittest.TestCase):
    def test_bfs(self):
        g = {"a":["b","c"],"b":["d"],"c":[],"d":[]}
        self.assertEqual(bfs(g,"a"), ["a","b","c","d"])
    def test_dfs(self):
        g = {"a":["b","c"],"b":["d"],"c":[],"d":[]}
        self.assertEqual(dfs(g,"a"), ["a","b","d","c"])
    def test_dijkstra(self):
        g = {"a":[("b",1),("c",4)],"b":[("c",2)],"c":[]}
        self.assertEqual(dijkstra(g,"a"), {"a":0,"b":1,"c":3})
    def test_disconnected(self):
        g = {"a":[("b",1)],"c":[]}
        self.assertEqual(dijkstra(g,"a"), {"a":0,"b":1})
    def test_negative_rejected(self):
        g = {"a":[("b",-1)]}
        with self.assertRaises(ValueError):
            dijkstra(g,"a")
