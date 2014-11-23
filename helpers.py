# -*- coding: utf-8 -*-

import re
from version import __version__


class UnknownOperatorError(ValueError):
    pass


class UnknownREFlagError(ValueError):
    pass


class RegExp(object):
    """ Implements Regular expressions for searching into containers
    """

    def __init__(self, regexp, flags='', match=False):
        """ You can specify re flags via keyword argument or inside the re itself (?aiLmsux).
            Default evaluation mode is search, you can specify match via keyword argument.
        """
        self.match = match
        re_flags = 0
        try:
            for f in flags.lower():
                re_flags |= self.flags_dict[f]
        except KeyError:
            raise UnknownREFlagError("Reg Exp flag %s unknown" % f)
        self.re = re.compile(regexp, re_flags)

    def __call__(self, record, match=False):
        match = match or self.match
        if match:
            return self.re.match(record)
        return self.re.search(record)

    flags_dict = dict(
        i=re.I, l=re.L, m=re.M,
        s=re.S, u=re.U, x=re.X
    )
    if hasattr(re, 'A'):
        flags_dict['a'] = re.A


class Where(object):
    """
    Implements 'where' features for search into containers
    """

    def __init__(self, *terms, **kwargs):
        """ Terms is a list of dictionaries
            representing a disjunction (or) of conjunctions (and).
            Alternatively, you can specify kwargs only, resulting in a single term.
            The '_key_missing_' optional keyword allows to control missing keys behaviour:
            True: missing key behaves like True, False, it behaves like False, None it raises a KeyError
        """
        self.missing = kwargs.pop('_key_missing_', False)
        if terms and kwargs:
            raise ValueError("You must specify terms or kwags, not both")
        self.terms = []
        for t in terms:
            self.add_term(t)
        self.add_term(kwargs)

    def add_term(self, fields):
        if not fields:
            return
        term = []
        self.terms.append(term)
        for k, v in fields.iteritems():
            try:
                field, op = k.split('__')
            except ValueError:
                field, op = k, 'eq'
            if op == 'search':
                val = RegExp(v)
            elif op == 'match':
                val = RegExp(v, match=True)
            else:
                val = v
            try:
                op = self.operators[op]
            except KeyError:
                raise UnknownOperatorError("Operator '%s'" % op)
            term.append((field, op, val))

    def missing_manager(func):
        def wrapped(*args):
            try:
                return func(*args)
            except KeyError:
                self = args[0]
                if self.missing is None:
                    raise
                return self.missing

        return wrapped

    # comparators for all types

    @missing_manager
    def equals(self, record, field, value):
        return type(value)(record[field]) == value

    @missing_manager
    def notequals(self, record, field, value):
        return type(value)(record[field]) != value

    # comparators for numerical types

    @missing_manager
    def gt(self, record, field, value):
        return type(value)(record[field]) > value

    @missing_manager
    def gte(self, record, field, value):
        return type(value)(record[field]) >= value

    @missing_manager
    def lt(self, record, field, value):
        return type(value)(record[field]) < value

    @missing_manager
    def lte(self, record, field, value):
        return type(value)(record[field]) <= value

    @missing_manager
    def inrange(self, record, field, value):
        lo, hi = value
        t = type(lo)
        assert t is type(hi)
        return lo <= t(record[field]) < hi

    @missing_manager
    def notinrange(self, record, field, value):
        return not self.inrange(record, field, value)

    # comparators for string types

    @missing_manager
    def iequals(self, record, field, value):
        return record[field].lower() == value

    @missing_manager
    def notiequals(self, record, field, value):
        return record[field].lower() != value

    @missing_manager
    def contains(self, record, field, value):
        return value in record[field]

    @missing_manager
    def notcontains(self, record, field, value):
        return value not in record[field]

    @missing_manager
    def icontains(self, record, field, value):
        return value in record[field].lower()

    @missing_manager
    def noticontains(self, record, field, value):
        return value not in record[field].lower()

    @missing_manager
    def startswith(self, record, field, value):
        return record[field].startswith(value)

    @missing_manager
    def notstartswith(self, record, field, value):
        return not record[field].startswith(value)

    @missing_manager
    def istartswith(self, record, field, value):
        return record[field].lower().startswith(value)

    @missing_manager
    def notistartswith(self, record, field, value):
        return not record[field].lower().startswith(value)

    @missing_manager
    def endswith(self, record, field, value):
        return record[field].endswith(value)

    @missing_manager
    def notendswith(self, record, field, value):
        return not record[field].endswith(value)

    @missing_manager
    def iendswith(self, record, field, value):
        return record[field].lower().endswith(value)

    @missing_manager
    def notiendswith(self, record, field, value):
        return not record[field].lower().endswith(value)

    @missing_manager
    def regexp(self, record, field, value):
        return value(record[field])

    def __call__(self, record):
        return any(
            all(op(self, record, field, value) for field, op, value in t)
            for t in self.terms)

    operators = dict(
        equals=equals, eq=equals,
        iequals=iequals, ieq=iequals,
        notequals=notequals, neq=notequals,
        notiequals=notiequals, nieq=notiequals,
        gt=gt, gte=gte, lt=lt, lte=lte,
        inrange=inrange, range=inrange,
        notinrange=notinrange, nrange=notinrange,
        contains=contains, cont=contains,
        notcontains=notcontains, ncont=notcontains,
        icontains=icontains, icont=icontains,
        noticontains=noticontains, nicont=noticontains,
        startswith=startswith, start=startswith,
        notstartswith=notstartswith, nstart=notstartswith,
        istartswith=istartswith, istart=istartswith,
        notistartswith=notistartswith, nistart=notistartswith,
        endswith=endswith, end=endswith,
        notendswith=notendswith, nend=notendswith,
        iendswith=iendswith, iend=iendswith,
        notiendswith=notiendswith, niend=notiendswith,
        search=regexp, match=regexp,
    )
