"""Lightweight performance guard: prints OK when complexities hold."""
import time
from intervals import merge_intervals
from lru import LRUCache


def main():
    intervals = [[i, i + 1] for i in range(20000)]
    t = time.time()
    merge_intervals(intervals)
    merge_dt = time.time() - t

    c = LRUCache(1000)
    t = time.time()
    for i in range(50000):
        c.put(i % 2000, i)
        c.get(i % 2000)
    lru_dt = time.time() - t

    assert merge_dt < 2.0, f"merge too slow: {merge_dt:.3f}s (expected O(n log n))"
    assert lru_dt < 2.0, f"lru too slow: {lru_dt:.3f}s (expected O(1) ops)"
    print(f"OK merge={merge_dt:.3f}s lru={lru_dt:.3f}s")


if __name__ == "__main__":
    main()
