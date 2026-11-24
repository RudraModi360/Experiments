"""Min-heap priority queue."""
class MinHeap:
    def __init__(self):
        self.data = []
    def push(self, item):
        self.data.append(item)
        # BUG: no sift-up
    def pop(self):
        if not self.data: return None
        # BUG: removes last, not min
        return self.data.pop()
    def __len__(self):
        return len(self.data)
