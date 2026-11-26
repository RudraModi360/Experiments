_items = []
def add(item):
    # BUG 3: mutates input and appends duplicate
    _items.append(item)
    return list(_items)
def all_items():
    return list(_items)
