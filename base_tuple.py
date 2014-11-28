# -*- coding: utf-8 -*-

from collections import Iterable

from mixins import CacheSetMixin


class atuple(tuple):
    # Fixme: must reimplement methods that return tuple (see __add__)
    """
    Replacement class for tuple, with compatible API.
    """
    _root_class = tuple

    def __new__(cls, *args):
        """ Replacement constructor, admits a single iterable or more than one parameter
        """
        if len(args) == 1 and isinstance(args[0], Iterable):
            return tuple.__new__(cls, args[0])
        else:
            return tuple.__new__(cls, args)

    def __add__(self, iterable):
        # Fixme: possible optimization in py3
        return self.__class__(tuple.__add__(self, tuple(iterable)))

    def last(self):
        try:
            return self[-1]
        except IndexError:
            pass

    def body(self):
        l = len(self) - 1
        return self.__class__(x for i, x in enumerate(self) if i < l)

    def first(self):
        try:
            return self[0]
        except IndexError:
            pass

    def tail(self):
        return self.__class__(x for i, x in enumerate(self) if i > 0)


class btuple(CacheSetMixin, atuple):
    pass
