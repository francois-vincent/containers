# -*- coding: utf-8 -*-

# TODO
# tester différentes implémentations (speed) ex: set.contains_all iterator vs set arithmetic
# éventuellement mettre 2 implémentations avec un test (comme dict.__and__)
# design a purely immutable dict class with history stored in deque
# voir lodash.js pour d'autres idées, voir https://pythonhosted.org/pysistence/
# tester en python 2 et python 3

from collections import defaultdict, Iterable
from bisect import bisect_left
from operator import add

from version import __version__


class DuplicateValueError(ValueError):
    pass


class ReverseDictFactory(object):
    """
    Helper class for dict.reverse()
    """

    class NoneObject(object):
        pass

    class _count(object):
        def __init__(self):
            self.value = 0

        def add(self, k, v):
            self.value += 1

        def val(self):
            return self.value

    class _list(list):
        def add(self, k, v):
            self.append(k)

        def val(self):
            return self

    class _raise(object):
        def __init__(self):
            self.value = ReverseDictFactory.NoneObject

        def add(self, k, v):
            if self.value is not ReverseDictFactory.NoneObject:
                raise DuplicateValueError("Duplicate value '%s' found for keys '%s' and '%s'" % (v, k, self.value))
            self.value = k

        def val(self):
            return self.value

    @classmethod
    def get_dict(cls, case):
        return defaultdict({
            'raise': cls._raise,
            'count': cls._count,
            'list': cls._list,
        }[case])


class FilterMixin(object):

    # immutable methods (return another self)

    def filter(self, f=bool, negate=False):
        """ Returns a copy of self, retaining elements that satisfy f.
        """
        cls = getattr(self, 'iterable', self.__class__)
        if negate:
            return cls(x for x in self if not f(x))
        else:
            return cls(x for x in self if f(x))

    # helper methods (return a value)

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
        """ True if every element of iterable is a key of self
            use preferably if self.__contains__() evaluates in constant time
        """
        return all(i in self for i in iterable)

    def contains_any(self, iterable):
        """ True if any element of iterable is a key of self
            use preferably if self.__contains__() evaluates in constant time
        """
        return any(i in self for i in iterable)

    def all_in(self, container):
        """ True if all keys of self are also in container
            use preferably if container.__contains__() evaluates in constant time
        """
        return all(i in container for i in self)

    def any_in(self, container):
        """ True if any key of self are also in container
            use preferably if container.__contains__() evaluates in constant time
        """
        return any(i in container for i in self)

    def reduce(self, f=bool):
        """ Returns the sum of the values of f calculated on each element
            if f returns a boolean, this counts the number of elements that satisfy f
        """
        return reduce(add, (f(x) for x in self))

    count = reduce


class ftuple(FilterMixin, tuple):
    """
    Replacement class for tuple, with better API and many useful methods.
    Many new methods have been added, they are classified as immutable, muttable and helpers
    """
    root = tuple

    def __new__(cls, *args):
        """ Replacement constructor, Python API is not coherent:
            dict() admits a dict or **kwarsgs, so tuple() should admit an iterable or *args
        """
        if len(args) == 1 and isinstance(args[0], Iterable):
            return tuple.__new__(cls, args[0])
        else:
            return tuple.__new__(cls, args)


class flist(FilterMixin, list):
    """
    Replacement class for list, with better API and many useful methods.
    In place methods return 'self' instead of None, better for chaining and returning
    Many new methods have been added, they are classified as immutable, muttable and helpers
    """
    root = list

    def __init__(self, *args):
        """ Replacement constructor, Python API is not coherent:
            dict() admits a dict or **kwarsgs, so list() should admit an iterable or *args
        """
        if len(args) == 1 and isinstance(args[0], Iterable):
            list.__init__(self, args[0])
        else:
            list.__init__(self, args)

    # mutable methods (return self)

    def clear(self):
        """ clear replacement that returns self
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

    def insert(self, i, x):
        """ insert replacement that corrects negative index behaviour of original (can not append)
        """
        if i < 0:
            if i == -1:
                return self.append(x)
            i += 1
        list.insert(self, i, x)
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

    def __add__(self, iterable):
        """ Immutable version of extend
        """
        return flist(self).extend(iterable)

    def __sub__(self, iterable):
        # Fixme: optimize
        """ Immutable version of discard_all
        """
        return flist(self).discard_all(iterable)

    # helper methods (return a value)

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


class fdict(FilterMixin, dict):
    """
    Replacement class for dict, with better API and many useful methods.
    In place methods return 'self' instead of None, better for chaining and returning
    Many new methods have been added, they are classified as immutable, muttable and helpers
    """
    root = dict
    __default_value__ = None

    # mutable methods (return self)

    def clear(self):
        dict.clear(self)
        return self

    def update(self, E={}, **F):
        """ Update replacement that retuurns sel
        """
        dict.update(self, E, **F)
        return self

    replace = update

    def update_difference(self, mapping):
        """ Like update except that only new keys will be updated
        """
        for k, v in mapping.iteritems():
            if k in self:
                continue
            self[k] = v
        return self

    def remove(self, elt):
        """ Alias of delete that returns self
        """
        self.__delitem__(elt)
        return self

    def remove_all(self, iterable):
        """ iterable version of remove
        """
        for k in iterable:
            self.__delitem__(k)
        return self

    def discard(self, elt):
        """ Like delete except it does not raise KeyError exception
        """
        if elt in self:
            self.__delitem__(elt)
        return self

    def discard_all(self, iterable):
        """ Iterable version of discard
        """
        for k in iterable:
            if k in self:
                self.__delitem__(k)
        return self

    def project(self, iterable):
        """ Removes every key of self that is not in iterable
        """
        for k in set(self) - set(iterable):
            self.__delitem__(k)
        return self

    def __iadd__(self, other):
        """ Like update, except that it can add any iterable
        """
        if not isinstance(other, dict):
            other = dict.fromkeys(other, fdict.__default_value__)
        return self.update(other)

    __ior__ = __iadd__
    __isub__ = discard_all
    __iand__ = __imul__ = project

    # immutable methods (return another dict)

    def filter_dict(self, f=ftuple, negate=False):
        """ Returns a copy of self filtered by f(key, value)
        """
        if negate:
            return fdict((k, v) for k, v in self.iteritems() if not f(k, v))
        else:
            return fdict((k, v) for k, v in self.iteritems() if f(k, v))

    def reverse(self, duplicate=None):
        """ reverse the dictionary (exchange keys and values)
            what's happening to duplicate values ?
            if duplicate == None, an arbitrary value among duplicates is chosen (fastest)
            if duplicate == 'raise', raise a detailed DuplicateValueError exception
            if duplicate == 'count', count number of keys (for duplicates, this number is >1)
            if duplicate == 'list', append keys in a list
        """
        if not duplicate:
            return fdict((v, k) for k, v in self.iteritems())
        data = ReverseDictFactory.get_dict(duplicate)
        for k, v in self.iteritems():
            data[v].add(k, v)
        return fdict((k, v.val()) for k, v in data.iteritems())

    def add_difference(self, other):
        """ Immutable version of update_difference, that can add any iterable
        """
        if not isinstance(other, dict):
            other = dict.fromkeys(other, fdict.__default_value__)
        return fdict(self).update_difference(other)

    def __add__(self, other):
        """ Immutable version of update, that can add any iterable
        """
        if not isinstance(other, dict):
            other = dict.fromkeys(other, fdict.__default_value__)
        return fdict(self).update(other)

    def __sub__(self, other):
        # Fixme: optimize
        """ Immutable version of discard_all
        """
        return fdict(self).discard_all(other)

    def __and__(self, other):
        """ Immutable version of project, with optimization based on the relative size
        """
        if len(other) > len(self) and isinstance(other, dict):
            return fdict((k, v) for k, v in self.iteritems() if k in other)
        else:
            return fdict((k, self[k]) for k in other if k in self)

    __or__ = __add__
    __mul__ = __and__


class fset(FilterMixin, set):
    # Fixme: complete methods set
    """
    Replacement class for set
    In place methods return 'self' instead of None
    - __iadd__: accepts any iterable, not only lists
    """
    root = set

    def __init__(self, *args):
        """ Replacement constructor, Python API is not coherent:
            dict() admits a dict or **kwarsgs, so set() should admit an iterable or *args
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
        set.update(self, set(iterable))
        return self

    __iadd__ = __ior__ = update

    # immutable methods (return another set)

    def __or__(self, iterable):
        return fset(self).update(iterable)

    __add__ = __or__

fdict.iterable = fset
