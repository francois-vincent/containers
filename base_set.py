# -*- coding: utf-8 -*-

from collections import Iterable


class aset(set):
    # Fixme: complete methods set
    # Fixme: draw a table of features (adding, removing, etc) with method names for mutable and immutable
    """
    Replacement class for set, with better API and many useful methods.
    In place methods return 'self' instead of None, better for chaining and returning.
    Many new methods have been added, they are classified as immutable, muttable and predicates.
    """
    _root_class = set

    def __init__(self, *args):
        """ Replacement constructor, Python API is not coherent:
            dict() admits a dict or **kwargs, so set() should admit an iterable or *args
        """
        if len(args) == 1 and isinstance(args[0], Iterable):
            set.__init__(self, args[0])
        else:
            set.__init__(self, args)

    # mutable methods (return self)

    def add(self, item):
        set.add(item)
        return self

    def clear(self):
        set.clear(self)
        return self

    def update(self, iterable):
        set.update(self, iterable)
        return self

    def remove(self, item):
        set.remove(self, item)
        return self

    def discard(self, item):
        set.discard(self, item)
        return self

    __iadd__ = __ior__ = update

    # immutable methods (return another set)

    def __add__(self, iterable):
        return self.__class__(self).update(iterable)

    def __sub__(self, iterable):
        return self.__class__(x for x in self if x not in iterable)

    __or__ = __add__
