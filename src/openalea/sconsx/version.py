#  -*- coding: utf-8 -*-

major = 2
"""(int) Version major component."""

minor = 4
"""(int) Version minor component."""

post = 1
"""(int) Version post or bugfix component."""

__version__ = ".".join([str(s) for s in (major, minor, post)])
