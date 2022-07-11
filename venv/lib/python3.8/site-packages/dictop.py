from functools import partial

VERSION = "0.2.1"

def select(target, path, default=None, slient=True):
    """Select item with path from target. 

    If not find item and slient marked as True, return default value.
    If not find item and slient marked as False, raise KeyError.
    """
    def _(value, slient):
        if slient:
            return value
        else:
            raise KeyError("")
    default = partial(_, default, slient)
    names = path.split(".")
    node = target
    for name in names:
        if isinstance(node, dict):
            try:
                node = node[name]
            except:
                return default()
        elif isinstance(node, list) and name.isdigit():
            try:
                node = node[int(name)]
            except:
                return default()
        elif hasattr(node, name):
            node = getattr(node, name)
        else:
            return default()
    return node


def listpad(thelist, length, fill=None):
    pad = length - len(thelist)
    if pad > 0:
        for _ in range(pad):
            thelist.append(fill)
    return thelist

def update(target, path, value):
    """Update item in path of target with given value.
    """
    names = path.split(".")
    names_length = len(names)
    node = target
    for index in range(names_length):
        name = names[index]
        if index == names_length - 1:
            last = True
        else:
            last = False
        if isinstance(node, dict):
            if last:
                node[name] = value
                return
            else:
                if not name in node:
                    node[name] = {}
                node = node[name]
        elif isinstance(node, list):
            name = int(name)
            listpad(node, name+1)
            if last:
                node[name] = value
                return
            else:
                node[name] = {}
                node = node[name]
        else:
            if last:
                setattr(node, name, value)
            else:
                setattr(node, name, {})
                node = getattr(node, name)
     