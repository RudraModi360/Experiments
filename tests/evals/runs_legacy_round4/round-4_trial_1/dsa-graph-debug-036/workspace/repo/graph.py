"""Graph algorithms."""
from collections import deque

def bfs(graph, src):
    # BUG: doesn't track visited, infinite loop risk
    q = deque([src])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph.get(u, []):
            q.append(v)
    return order

def dfs(graph, src):
    # BUG: recursion without visited
    res = []
    def _dfs(u):
        res.append(u)
        for v in graph.get(u, []):
            _dfs(v)
    _dfs(src)
    return res

def dijkstra(graph, src):
    # Validates non-negative edge weights and computes shortest paths in O((V+E) log V)
    import heapq
    if src not in graph and graph:
        # If src is not in graph keys at all, return {src: 0} if graph is empty, or handle accordingly
        pass

    dist = {src: 0}
    pq = [(0, src)]
    
    # Check edges for negative weights
    for u, neighbors in graph.items():
        for v, w in neighbors:
            if w < 0:
                raise ValueError("Negative edge weight encountered")

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist
