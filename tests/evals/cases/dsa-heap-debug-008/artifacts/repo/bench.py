import time, random
from heap import MinHeap
from dijkstra import shortest_paths
random.seed(1)
h = MinHeap()
for _ in range(1000):
    h.push(random.random())
for _ in range(1000):
    h.pop()
g = {str(i): [(str(j), random.random()) for j in range(i+1, min(i+5, 200))] for i in range(200)}
t=time.time(); shortest_paths(g,"0"); print("OK", round(time.time()-t,4))
