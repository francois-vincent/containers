# -*- coding: utf-8 -*-

from collections import defaultdict


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


class adict(dict):
    """
    Replacement class for dict, with better API and many useful methods.
    In place methods return 'self' instead of None, better for chaining and returning.
    Many new methods have been added, they are classified as immutable, muttable and helpers.
    """
    _root_class = dict
    _default_value = None
    # Fixme: should be aset or a derivative, but wich one ?
    _filter_constructor = set

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
            if k not in self:
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
            other = dict.fromkeys(other, self._default_value)
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
            return self.__class__((v, k) for k, v in self.iteritems())
        data = ReverseDictFactory.get_dict(duplicate)
        for k, v in self.iteritems():
            data[v].add(k, v)
        return self.__class__((k, v.val()) for k, v in data.iteritems())

    def add_difference(self, iterable):
        """ Immutable version of update_difference, that can add any iterable
        """
        # Fixme: optimize
        if not isinstance(iterable, dict):
            iterable = dict.fromkeys(iterable, self._default_value)
        return self.__class__(self).update_difference(iterable)

    def __add__(self, iterable):
        """ Immutable version of update, that can add any iterable
        """
        if not isinstance(iterable, dict):
            iterable = dict.fromkeys(iterable, self._default_value)
        return self.__class__(self).update(iterable)

    def __sub__(self, iterable):
        """ Immutable version of discard_all
        """
        return self.__class__((k, v) for k, v in self.iteritems() if k not in iterable)

    def __and__(self, iterable):
        """ Immutable version of project, with optimization based on the relative size
        """
        # Fixme: find a better criterium
        if len(iterable) > len(self) and isinstance(iterable, dict):
            return self.__class__((k, v) for k, v in self.iteritems() if k in iterable)
        else:
            return self.__class__((k, self[k]) for k in iterable if k in self)

    __or__ = __add__
    __mul__ = __and__
