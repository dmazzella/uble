try:
    from collections import namedtuple, OrderedDict, deque, defaultdict
except ImportError:
    try:
        from ucollections import namedtuple, OrderedDict, deque
    except ImportError:
        from ucollections import namedtuple, OrderedDict
        if "deque" not in globals():
            from .deque import deque
if "defaultdict" not in globals():
    from .defaultdict import defaultdict
