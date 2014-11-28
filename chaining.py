# -*- coding: utf-8 -*-


class Chain(object):
    """
    Allows to chain methods of mutable builtins or custom classes,
    without the hassle of derivating classes, wich can be quite tricky for builtins,
    see: http://yauhen.yakimovich.info/blog/2011/08/12/wrapping-built-in-python-types/
    Moreover, a chaining derivative of eg tuple, requires to recast the result of any
    cloning method to the derivative, wich is O(n). Instead, the recasting of a Chain
    instance is O(1).
    Avoid use on immutable builtins (useless).
    """

    def __init__(self, obj, mutable=True):
        self.object = obj
        self.mutable = mutable

    def __getattr__(self, item):
        def method(*args, **kwarsg):
            ret = getattr(self.object, item)(*args, **kwarsg)
            # methods returning NOne or self are chained with same wrapper/object
            if ret is None or ret is self.object:
                return self
            # mutable classes have their muted result instances recasted,
            # resulting in a new wrapper/object
            if self.mutable and isinstance(ret, self.object.__class__):
                return self._push(ret)
            return ret
        return method

    def _push(self, object):
        return self.__class__(object)

    def __str__(self):
        return str(self.object)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.object)


class ArturoChain(Chain):
    """
    This class does not recast immutable results, it simply changes inner instance
    """

    def _push(self, obj):
        self.object = obj
        return self


class HistoryChain(Chain):
    """
    This class changes inner instance and records past instances
    """

    def __init__(self, obj, mutable=True):
        Chain.__init__(self, obj, mutable)
        self.history = [obj]

    def _push(self, obj):
        self.object = obj
        self.history.append(obj)
        return self

    def backward(self):
        self.history.pop()
        self.object = self.history[-1]
        return self
