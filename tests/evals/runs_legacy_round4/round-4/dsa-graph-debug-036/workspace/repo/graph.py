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
    import heapq
    if src not in graph and graph:
        # If src not in graph at all, handle or return {src: 0} depending on convention,
        # but let's check negative weights across all edges first.
        pass
    
    # Check for negative edge weights and validate graph
    for u, neighbors in graph.items():
        for item in neighbors:
            if len(item) == 2:
                v, w = item
            else:
                v, w = item[0], item[1] # or handle accordingly
            if w < 0:
                raise ValueError("Negative edge weights not allowed in Dijkstra's algorithm")

    dist = {src: 0}
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        for edge in graph.get(u, []):
            v, w = edge[0], edge[1]
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist
