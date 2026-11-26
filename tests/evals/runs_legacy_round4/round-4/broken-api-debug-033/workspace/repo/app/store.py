_items = []
def add(item):
    if item not in _items:
        _items.append(item)
    return list(_items)
def all_items():
    return list(_items)
