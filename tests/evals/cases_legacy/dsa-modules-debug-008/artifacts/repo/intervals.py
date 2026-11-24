"""Merge overlapping intervals. Required complexity: O(n log n)."""


def merge_intervals(intervals):
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        last_end = merged[-1][1]
        if start >= last_end:   # BUG: >= splits touching intervals [1,2],[2,3]; must be >
            merged.append([start, end])
        else:
            merged[-1][1] = max(last_end, end)
    return merged
