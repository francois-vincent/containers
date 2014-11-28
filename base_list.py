# -*- coding: utf-8 -*-

from collections import Iterable

from helpers import mixin_factory


class alist(list):
    """
    Replacement class for list, with compatible API.
    In place methods are redefined to return 'self' instead of None.
    """
    _root_class = list

    def __init__(self, *args):
        """ Replacement constructor, admits a single iterable or more than one parameter
        """
        if len(args) == 1 and isinstance(args[0], Iterable):
            list.__init__(self, args[0])
        else:
            list.__init__(self, args)

    # mutable methods (return self)

    def clear(self):
        """ clear returns self
        """
        del self[:]
        return self

    def append(self, x):
        """ append replacement that returns self
        """
        list.append(self, x)
        return self

    def extend(self, iterable):
        """ extend replacement that returns self
        """
        list.extend(self, iterable)
        return self

    def remove(self, value):
        """ remove replacement that returns self
        """
        list.remove(self, value)
        return self

    def remove_all(self, iterable):
        """ iterable version of remove
        """
        for i in iterable:
            list.remove(self, i)
        return self

    def remove_index(self, at):
        del self[at]
        return self

    def remove_slice(self, start=0, end=None):
        """ Does not raise IndexError
        """
        if end is None:
            del self[start:]
        else:
            del self[start:end]
        return self

    def discard(self, value):
        """ Like remove except it does not raise ValueError exception
        """
        try:
            list.remove(self, value)
        except ValueError:
            pass
        return self

    def discard_all(self, iterable):
        """ iterable version of discard
        """
        for i in iterable:
            self.discard(i)
        return self

    def discard_index(self, at):
        try:
            del self[at]
        except IndexError:
            pass
        return self

    discard_slice = remove_slice

    def reverse(self):
        """ reverse replacement that returns self
        """
        list.reverse()
        return self

    def sort(self, **p):
        """ sort replacement that returns self
        """
        list.sort(self, **p)
        return self

    __isub__ = discard_all

    # immutable methods (return another list)

    def head(self):
        try:
            return self[-1]
        except IndexError:
            pass

    def tail(self):
        try:
            return self[:-1]
        except IndexError:
            pass

    def __add__(self, iterable):
        """ Immutable version of extend
        """
        return self.__class__(self).extend(iterable)

    def __sub__(self, iterable):
        """ Immutable version of discard_all
        """
        return self.__class__(x for x in self if x not in iterable)


class ListInsertMixin(object):
    """
    Redefines insert for a subclass of list.
    This is isolated into a mixin because the API is a bit changed:
    The origin of negative indexes is so that -1 does an append.
    """

    def insert(self, i, x):
        """ insert replacement that corrects negative index behaviour of original (does not append)
        """
        if i < 0:
            if i == -1:
                return self.append(x)
            i += 1
        list.insert(self, i, x)
        return self

blist = mixin_factory('blist', ListInsertMixin, alist)