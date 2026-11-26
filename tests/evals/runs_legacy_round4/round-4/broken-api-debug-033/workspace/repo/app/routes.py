from .store import add, all_items

def handle_request(req):
    action = req.get("action")
    if action == "add":
        item = req.get("item")
        if item is not None:
            add(item)
            return {"status": "ok"}
    elif action == "list":
        return {"items": all_items()}
    return {"status": "error"}
