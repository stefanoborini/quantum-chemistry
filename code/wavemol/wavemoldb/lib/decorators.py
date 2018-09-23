def reportCall(fn):
    from itertools import chain
    def wrapped(*v, **k):
        name = fn.__name__
        print "%s(%s)" % (name, ", ".join(map(repr, chain(v, k.values()))))
        return fn(*v, **k)
    return wrapped
