# -*- coding: utf-8 -*-

import unittest

from chaining import Chain, ArturoChain, HistoryChain


class toto(object):
    def a(self):
        return self
    def b(self):
        return None
    def c(self):
        return 1
    def d(self):
        return self.__class__()


class ChainTestCase(unittest.TestCase):

    def test_mutable(self):
        l = [1, 2, 3]
        ll = list(l)
        c = Chain(ll)
        self.assertIs(c.append('x').__iadd__((4, 5)).extend('ab'), c)
        self.assertListEqual(c.object, ll)
        self.assertListEqual(ll, l + ['x', 4, 5, 'a', 'b'])

    def test_immutable(self):
        l = [1, 2, 3]
        ll = list(l)
        c = Chain(ll)
        cc = c.__add__([4, 5])
        self.assertIsNot(cc, c)
        self.assertIsInstance(cc, Chain)
        self.assertListEqual(cc.object, l + [4, 5])
        self.assertListEqual(ll, l)

    def test_mutable_a(self):
        o = toto()
        c = Chain(o)
        cc = c.a()
        self.assertIs(cc, c)

    def test_mutable_b(self):
        o = toto()
        c = Chain(o)
        cc = c.b()
        self.assertIs(cc, c)

    def test_immutable_c(self):
        o = toto()
        c = Chain(o)
        cc = c.c()
        self.assertIs(cc, 1)

    def test_immutable_d(self):
        o = toto()
        c = Chain(o)
        cc = c.d()
        self.assertIsInstance(cc, Chain)
        self.assertIsNot(cc, c)


class ArturoChainTestCase(unittest.TestCase):

    def test_immutable_d(self):
        o = toto()
        c = ArturoChain(o)
        cc = c.d()
        self.assertIs(cc, c)


class HistoryChainTestCase(unittest.TestCase):

    def test_immutable_d(self):
        o = toto()
        c = HistoryChain(o)
        cc = c.d()
        self.assertIs(cc, c)
        self.assertIsNot(cc.object, o)
        self.assertIs(cc.backward().object, o)


if __name__ == '__main__':
    unittest.main()
