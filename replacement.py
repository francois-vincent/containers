# -*- coding: utf-8 -*-

"""
This module offers to replace builtins tuple, list, dict and set with their fcontainers equivalents.
Just drop "from replacement import *" at top of file and start using new features in your code.
Fcontainers have their API compatible with their original counterparts.
Fcontainers containers can be moved to and from other modules without any effect (except possibly
 subtle difference of deriving from (dict or list etc) instead of being a (dict or list etc)).
"""

__all__ = ['tuple', 'dict', 'list', 'set']

from fcontainers import ftuple, fdict, flist, fset

tuple, dict, list, set = ftuple, fdict, flist, fset
