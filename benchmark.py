# -*- coding: utf-8 -*-

from timeit import timeit

print timeit("'z' in t", "from base_tuple import atuple; t=atuple('az')")
print timeit("'z' in t", "from base_tuple import btuple; t=btuple('az')")
print timeit("'z' in t", "from base_tuple import atuple; t=atuple('a'*20 + 'z')")
print timeit("'z' in t", "from base_tuple import btuple; t=btuple('a'*20+'z')")
print timeit("'z' in t", "from base_tuple import atuple; t=atuple('a'*40 + 'z')")
print timeit("'z' in t", "from base_tuple import btuple; t=btuple('a'*40+'z')")
