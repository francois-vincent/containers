# -*- coding: utf-8 -*-

from helpers import add_attribute_self, yesman
from collections import defaultdict, Iterable
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
        """ Returns a copy of self, only retaining elements that satisfy f.
        """
        cls = getattr(self, 'iterable', self.__class__)
        if negate:
            return cls(x for x in self if not f(x))
        else:
            return cls(x for x in self if f(x))

    def filter_index(self, f=yesman, negate=False):
        """ Returns a copy of self, only retaining index/elements pairs that satisfy f.
        """
        cls = getattr(self, 'iterable', self.__class__)
        if negate:
            return cls(x for i, x in enumerate(self) if not f(i, x))
        else:
            return cls(x for i, x in enumerate(self) if f(i, x))

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

    count = reduce


@add_attribute_self('iterable')
class ftuple(FilterMixin, tuple):
    # Fixme: optimize all_in, any_in (use a cached set ?)
    """
    Replacement class for tuple, with better API and many useful methods.
    Many new methods have been added, they are classified as immutable, muttable and helpers
    """
    root = tuple

    def __new__(cls, *args):
        """ Replacement constructor, Python API is not coherent:
            dict() admits a dict or **kwargs, so tuple() should admit an iterable or *args
        """
        if len(args) == 1 and isinstance(args[0], Iterable):
            return tuple.__new__(cls, args[0])
        else:
            return tuple.__new__(cls, args)

    def __sub__(self, other):
        """ Returns a copy of self with element elem removed
        """
        pass

    def sub_index(self, index):
        """ Returns a copy of self with element @index removed
        """
        pass


@add_attribute_self('iterable')
class flist(FilterMixin, list):
    """
    Replacement class for list, with better API and many useful methods.
    In place methods return 'self' instead of None, better for chaining and returning
    Many new methods have been added, they are classified as immutable, muttable and helpers
    """
    root = list

    def __init__(self, *args):
        """ Replacement constructor, Python API is not coherent:
            dict() admits a dict or **kwargs, so list() should admit an iterable or *args
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

    def remove_slice(self, start=None, end=None):
        # best way to specify a slice in args
        # use filter_index ?
        pass

    def discard_slice(self, start=None, end=None):
        pass

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


@add_attribute_self('iterable')
class fset(FilterMixin, set):
    # Fixme: complete methods set
    # Fixme: draw a table of features (adding, removing, etc) with method names for mutable and immutable
    """
    Replacement class for set, with better API and many useful methods.
    In place methods return 'self' instead of None, better for chaining and returning.
    Many new methods have been added, they are classified as immutable, muttable and predicates.
    """
    root = set

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
        return fset(self).update(iterable)

    def __sub__(self, iterable):
        return fset(self)

    __or__ = __add__


class fdict(FilterMixin, dict):
    """
    Replacement class for dict, with better API and many useful methods.
    In place methods return 'self' instead of None, better for chaining and returning.
    Many new methods have been added, they are classified as immutable, muttable and helpers.
    """
    root = dict
    __default_value__ = None
    iterable = fset

    # mutable methods (return self)

    def clear(self):
        dict.clear(self)
        return self

    def update(self, E={}, **F):
        """ Update replacement that retuurns sel
        """
        dict.update(self, E, **F)
        return self

    replace = update  # updating an existing key does a replacement, so this alias

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
