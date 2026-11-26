import time, random
from graph import dijkstra
random.seed(1)
g = {str(i): [(str(j), random.random()) for j in range(i+1, min(i+5, 200))] for i in range(200)}
t=time.time(); dijkstra(g,"0"); print("OK", round(time.time()-t,4))
