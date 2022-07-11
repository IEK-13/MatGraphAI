# coding: utf-8
import inspect
import importlib
from dictop import select


def get_caller_globals():
    """
    获取当前函数调用者的globals。
    例如：
        def a():
            x = 2
            b()
        def b():
            x = 3
            y = get_caller_globals()
        a()
    上述代码中
        当前函数：b
        调用者：a
        y中的globals为a函数所处上下文中的globals
    """
    frame = inspect.currentframe()
    try:
        return frame.f_back.f_back.f_globals
    finally:
        del frame

def get_caller_locals():
    """
    获取当前函数调用者的locals。
    例如：
        def a():
            x = 2
            b()
        def b():
            x = 3
            y = get_caller_globals()
        a()
    上述代码中
        当前函数：b
        调用者：a
        y中的globals为a函数所处上下文中的globals
    """
    frame = inspect.currentframe()
    try:
        return frame.f_back.f_back.f_locals
    finally:
        del frame

def import_module(path, root=None):
    """
    动态加载模块。
    仅能加载模块，不能加载模块中的类、对象、函数。
    加载失败返回NONE。
    """
    try:
        return importlib.import_module(path, root)
    except ImportError:
        return None

def import_from_string(path, slient=True):
    """
    根据给定的对象路径，动态加载对象。
    """
    names = path.split(".")
    for i in range(len(names), 0, -1):
        p1 = ".".join(names[0:i])
        module = import_module(p1)
        if module:
            p2 = ".".join(names[i:])
            if p2:
                return select(module, p2, slient=slient)
            else:
                return module
    name = names[0]
    names = names[1:]
    module = get_caller_locals().get(name)
    if module and names:
        return select(module, ".".join(names), slient=slient)
    if module:
        return module
    module = get_caller_globals().get(name)
    if module and names:
        return select(module, ".".join(names), slient=slient)
    if module:
        return module
    if slient:
        return None
    else:
        raise ImportError("Import {path} failed.".format(path=path))
