# -*- coding: utf-8 -*-

from collections import Iterable

from helpers import add_attribute_self, yesman


@add_attribute_self('filter_constructor')
class ftuple(tuple):
    """
    Replacement class for tuple, with better API.
    In place methods return 'self' instead of None, better for chaining and returning
    """
    root = tuple

    def __new__(cls, *args):
        """ Replacement constructor, admits a single iterable or more than one parameter
        """
        if len(args) == 1 and isinstance(args[0], Iterable):
            return tuple.__new__(cls, args[0])
        else:
            return tuple.__new__(cls, args)


@add_attribute_self('filter_constructor')
class flist(list):
    """
    Replacement class for list, with compatible API.
    In place methods are redefined to return 'self' instead of None.
    """
    root = list

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
