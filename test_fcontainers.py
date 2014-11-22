# -*- coding: utf-8 -*-

from replacement import *
from fcontainers import DuplicateValueError
from helpers import Where, UnknownOperatorError, RegExp
import unittest


class DictTestCase(unittest.TestCase):

    def setUp(self):
        self.d = dict(a=1, b=2, c=3, d=4)

    def test_constructor(self):
        d = self.d
        self.assertDictEqual(dict(d), d)
        self.assertDictEqual(dict(d, **d), d)

    def test_clear(self):
        d = self.d
        self.assertDictEqual(d.clear(), {})

    def test_update(self):
        d = dict(self.d)
        self.assertDictEqual(dict().update(d), d)
        self.assertDictEqual(dict().update(**d), d)
        self.assertDictEqual(dict().update(d, **d), d)
        self.assertDictEqual(d.update(e=5), self.d + {'e': 5})
        self.assertDictEqual(d, self.d + {'e': 5})

    def test_discard(self):
        d = self.d
        self.assertDictEqual(d.discard('a'), dict(b=2, c=3, d=4))
        self.assertDictEqual(d, dict(b=2, c=3, d=4))
        self.assertDictEqual(d.discard('e'), dict(b=2, c=3, d=4))

    def test_discard_all(self):
        d = self.d
        self.assertDictEqual(d.discard_all('ad'), dict(b=2, c=3))
        self.assertDictEqual(d, dict(b=2, c=3))
        self.assertDictEqual(d.discard_all('bef'), dict(c=3))

    def test_remove(self):
        d = self.d
        self.assertDictEqual(d.remove('a'), dict(b=2, c=3, d=4))
        self.assertDictEqual(d, dict(b=2, c=3, d=4))
        self.assertRaises(KeyError, d.remove, 'e')

    def test_remove_all(self):
        d = self.d
        self.assertDictEqual(d.remove_all('ad'), dict(b=2, c=3))
        self.assertDictEqual(d, dict(b=2, c=3))
        self.assertRaises(KeyError, d.remove_all, 'bef')

    def test_contains_all(self):
        d = self.d
        self.assertTrue(d.contains_all('ab'))
        self.assertTrue(d.contains_all('abcd'))
        self.assertFalse(d.contains_all('abce'))

    def test_contains_any(self):
        d = self.d
        self.assertTrue(d.contains_any('defg'))
        self.assertFalse(d.contains_any('xyz'))

    def test_project(self):
        d = self.d
        self.assertDictEqual(d.project('bc'), dict(b=2, c=3))
        self.assertDictEqual(d, dict(b=2, c=3))
        self.assertDictEqual(d.project('bc'), dict(b=2, c=3))
        self.assertDictEqual(d.project('ad'), {})

    def test_reverse_noduplicate(self):
        d = dict(self.d)
        self.assertDictEqual(d.reverse(), {1: 'a', 2: 'b', 3: 'c', 4: 'd'})
        self.assertDictEqual(d, self.d)
        self.assertDictEqual(d.reverse().reverse(), self.d)

    def test_reverse_duplicate_noraise(self):
        d = self.d + dict(e=1)
        self.assertDictEqual(d.reverse() & (2, 3, 4), {2: 'b', 3: 'c', 4: 'd'})
        self.assertIn(d.reverse()[1], ('a', 'e'))

    def test_reverse_duplicate_raise(self):
        d = self.d + dict(e=1)
        self.assertRaises(DuplicateValueError, d.reverse, 'raise')

    def test_reverse_duplicate_count(self):
        d = self.d + dict(e=1)
        self.assertDictEqual(d.reverse('count'), {1: 2, 2: 1, 3: 1, 4: 1})

    def test_reverse_duplicate_list(self):
        d = self.d + dict(e=1)
        self.assertDictEqual(d.reverse('list'), {1: ['a', 'e'], 2: ['b'], 3: ['c'], 4: ['d']})

    def test_add(self):
        d = dict(self.d)
        self.assertDictEqual(d + 'ae', {'a': None, 'b': 2, 'c': 3, 'd': 4, 'e': None})
        self.assertDictEqual(d, self.d)
        d = dict(self.d)
        self.assertDictEqual(d + {'a': 9, 'e': 8}, {'a': 9, 'b': 2, 'c': 3, 'd': 4, 'e': 8})
        self.assertDictEqual(d, self.d)
        d = dict(self.d)
        self.assertDictEqual(d + dict(a=9, e=8), {'a': 9, 'b': 2, 'c': 3, 'd': 4, 'e': 8})
        self.assertDictEqual(d, self.d)

    def test_add_difference(self):
        d = dict(self.d)
        self.assertDictEqual(d.add_difference('ae'), {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': None})
        self.assertDictEqual(d, self.d)

    def test_sub(self):
        d = dict(self.d)
        self.assertDictEqual(d - 'ad', dict(b=2, c=3))
        self.assertDictEqual(d, self.d)
        self.assertDictEqual(d - 'adef', dict(b=2, c=3))

    def test_and(self):
        d = dict(self.d)
        self.assertDictEqual(d & 'bc', dict(b=2, c=3))
        self.assertDictEqual(d, self.d)
        self.assertDictEqual(d & 'ef', {})

    def test_iadd(self):
        d = dict(self.d)
        d += 'ae'
        self.assertDictEqual(d, {'a': None, 'b': 2, 'c': 3, 'd': 4, 'e': None})
        d = dict(self.d)
        d += {'a': 9, 'e': 8}
        self.assertDictEqual(d, {'a': 9, 'b': 2, 'c': 3, 'd': 4, 'e': 8})
        d = dict(self.d)
        d += dict(a=9, e=8)
        self.assertDictEqual(d, {'a': 9, 'b': 2, 'c': 3, 'd': 4, 'e': 8})

    def test_isub(self):
        d = self.d
        d -= 'ad'
        self.assertDictEqual(d, dict(b=2, c=3))

    def test_imul_iand(self):
        d = self.d
        d *= 'bc'
        self.assertDictEqual(d, dict(b=2, c=3))
        d &= 'xy'
        self.assertDictEqual(d, {})

    def test_filter(self):
        d = dict(self.d)
        self.assertEqual(set(d.filter()), set('abcd'))
        self.assertEqual(set(d.filter(f=lambda x: x != 'a')), set('bcd'))
        self.assertDictEqual(d, self.d)

    def test_filter_dict(self):
        d = dict(self.d)
        self.assertEqual(d.filter_dict(), d)
        self.assertEqual(d.filter_dict(f=lambda x, y: x != 'a'), d-'a')
        self.assertDictEqual(d, self.d)


class ListTestCase(unittest.TestCase):

    def test_constructor(self):
        self.assertListEqual(list('abcd'), ['a', 'b', 'c', 'd'])
        self.assertListEqual(list(list('abcd')), ['a', 'b', 'c', 'd'])

    def test_append_extend(self):
        l = list('ab')
        self.assertListEqual(l.append('c').extend('de'), ['a', 'b', 'c', 'd', 'e'])
        self.assertListEqual(l, ['a', 'b', 'c', 'd', 'e'])

    def test_insert(self):
        l = list('ab')
        self.assertListEqual(l.insert(0, 'x'), ['x', 'a', 'b'])
        self.assertListEqual(l.insert(-1, 'y'), ['x', 'a', 'b', 'y'])

    def test_remove(self):
        l = list('abc')
        self.assertListEqual(l.remove('a'), ['b', 'c'])
        self.assertRaises(ValueError, l.remove, 'a')

    def test_remove_all(self):
        l = list('abc')
        self.assertListEqual(l.remove_all('ac'), ['b'])
        self.assertRaises(ValueError, l.remove_all, 'bc')

    def test_discard(self):
        l = list('abc')
        self.assertListEqual(l.discard('a'), ['b', 'c'])
        self.assertListEqual(l.discard('a'), ['b', 'c'])

    def test_discard_all(self):
        l = list('abc')
        self.assertListEqual(l.discard_all('ac'), ['b'])
        self.assertListEqual(l.discard_all('ac'), ['b'])

    def test_add(self):
        self.assertListEqual(list('ab') + 'cd', ['a', 'b', 'c', 'd'])

    def test_iadd(self):
        l = list('ab')
        l += 'cd'
        self.assertListEqual(l, ['a', 'b', 'c', 'd'])

    def test_sub(self):
        self.assertListEqual(list('abcd') - 'cd', ['a', 'b'])
        self.assertListEqual(list('abcd') - 'cx', ['a', 'b', 'd'])

    def test_isub(self):
        l = list('abcd')
        l -= 'cd'
        self.assertListEqual(l, ['a', 'b'])
        l = list('abcd')
        l -= 'cx'
        self.assertListEqual(l, ['a', 'b', 'd'])

    def test_all_none(self):
        l1 = list((None, None, None))
        l2 = list((None, None, False))
        self.assertEqual(l1.all(f=lambda x: x is None), True)
        self.assertEqual(l2.all(f=lambda x: x is None), False)

    def test_get(self):
        l = list('abc')
        self.assertEqual(l.get(1), 'b')
        self.assertIsNone(l.get(10))
        self.assertEqual(l.get(-10, 'out'), 'out')


class SetTestCase(unittest.TestCase):

    def test_constructor(self):
        self.assertSetEqual(set('abcd'), set(['a', 'b', 'c', 'd']))
        self.assertSetEqual(set(set('abcd')), set(['a', 'b', 'c', 'd']))


class WhereTestCase(unittest.TestCase):

    def setUp(self):
        self.data = dict(
            name='toto',
            age='12',
        )

    def test_unknown_operator(self):
        self.assertRaises(UnknownOperatorError, Where, name__operator=0)

    def test_equal(self):
        data = self.data
        where = Where(name='toto', age=12)
        self.assertTrue(where(data))
        data['age'] = 12
        self.assertTrue(where(data))
        data['name'] = 'zorro'
        self.assertFalse(where(data))
        where = Where(name__neq='toto', age=12)
        self.assertTrue(where(data))

    def test_iequal(self):
        data = self.data.replace(name='TOTO')
        where = Where(name__ieq='toto', age=12)
        self.assertTrue(where(data))
        where = Where(name__ineq='toto', age=12)
        self.assertFalse(where(data))

    def test_contains(self):
        data = self.data
        where = Where(name__contains='to', age=12)
        self.assertTrue(where(data))

    def tetst_gt(self):
        data = self.data
        where = Where(name='toto', age__gt=10)
        self.assertTrue(where(data))
        where = Where(name='toto', age__gt=18)
        self.assertFalse(where(data))

    def test_inrange(self):
        data = self.data
        where = Where(name='toto', age__inrange=(10, 13))
        self.assertTrue(where(data))
        where = Where(name='toto', age__inrange=(10, 12))
        self.assertFalse(where(data))

    def test_missing_key(self):
        data = self.data
        where = Where(name='toto', value__inrange=(10, 13))
        self.assertFalse(where(data))
        where = Where(name='toto', value__inrange=(10, 13), _key_missing_=True)
        self.assertTrue(where(data))
        where = Where(name='toto', value__inrange=(10, 13), _key_missing_=None)
        self.assertRaises(KeyError, where, data)


class RegExpTestCase(unittest.TestCase):

    def test_search(self):
        re = RegExp('\d')
        self.assertTrue(re('xx10xx'))

    def test_match(self):
        re = RegExp('\d', match=True)
        self.assertFalse(re('xx10xx'))
        self.assertTrue(re('10xx'))


if __name__ == '__main__':
    unittest.main()