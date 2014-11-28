# -*- coding: utf-8 -*-

from bisect import bisect_left
from operator import add

from helpers import yesman


class GenericMixin(object):

    def filter(self, f=bool, negate=False):
        """ Returns a copy of self, only retaining elements that satisfy f.
            The returned object's class can be (or must be) different from the original class.
            This is specified in '_filter_constructor' optional class attribute.
        """
        cls = getattr(self, '_filter_constructor', self.__class__)
        if negate:
            return cls(x for x in self if not f(x))
        else:
            return cls(x for x in self if f(x))

    def first(self, f=bool, negate=False):
        """ Returns the first element that satisfies f.
        """
        if negate:
            for x in self:
                if not f(x):
                    return x
        else:
            for x in self:
                if f(x):
                    return x

    def all(self, f=bool):
        """ True if all elements satisfy f
        """
        return all(f(x) for x in self)

    def any(self, f=bool):
        """ True if any element satisfy f
        """
        return any(f(x) for x in self)

    def contains_all(self, iterable):
        """ True if every element (or key) of iterable is in self
            use preferably if self.__contains__() evaluates in constant time
        """
        return all(i in self for i in iterable)

    def contains_any(self, iterable):
        """ True if any element (or key) of iterable is in self
            use preferably if self.__contains__() evaluates in constant time
        """
        return any(i in self for i in iterable)

    def all_in(self, container):
        """ True if all elements (or keys) of self are also in container
            use preferably if container.__contains__() evaluates in constant time
        """
        return all(i in container for i in self)

    def any_in(self, container):
        """ True if any element (or key) of self are also in container
            use preferably if container.__contains__() evaluates in constant time
        """
        return any(i in container for i in self)

    def reduce(self, f=bool):
        """ Returns the sum of the values of f calculated on each element
            if f returns a boolean, this counts the number of elements that satisfy f
        """
        return reduce(add, (f(x) for x in self))


class IndexMixin(object):
    """
    Mixin suitable for tuple and list derivatives
    """

    def filter_index(self, f=yesman, negate=False):
        """ Returns a copy of self, only retaining index/elements pairs that satisfy f.
        """
        if negate:
            return self.__class__(x for i, x in enumerate(self) if not f(i, x))
        else:
            return self.__class__(x for i, x in enumerate(self) if f(i, x))

    def get(self, pos, default=None):
        """ Equivalent of dict.get for list: returns a default value if index is out of range
        """
        try:
            return self[pos]
        except IndexError:
            return default

    def index_b(self, value, start=0, stop=None):
        """ Performs binary search on sorted lists
        """
        if stop is None:
            stop = len(self)
        i = bisect_left(self, value, start, stop)
        if i < len(self) and self[i] == value:
            return i
        return -1

    def index_f(self, start=0, f=bool, negate=False):
        """ Returns the index of the first element that satisfies f
        """
        if negate:
            for i in xrange(start, len(self)):
                if not f(self[i]):
                    return i
            return -1
        else:
            for i in xrange(start, len(self)):
                if f(self[i]):
                    return i
            return -1


class MappingMixin(object):
    """
    Mixin suitable for dict derivatives
    """

    def filter_dict(self, f=yesman, negate=False):
        """ Returns a copy of self filtered by f(key, value)
        """
        if negate:
            return self.__class__((k, v) for k, v in self.iteritems() if not f(k, v))
        else:
            return self.__class__((k, v) for k, v in self.iteritems() if f(k, v))


class CacheSetMixin(object):
    """
    Mixin used to have a constant search time.
    Use only if length is > 20
    """

    def __init__(self, *args):
        super(CacheSetMixin, self).__init__(*args)
        self._set_cache = set(self)

    def __contains__(self, item):
        return item in self._set_cache
