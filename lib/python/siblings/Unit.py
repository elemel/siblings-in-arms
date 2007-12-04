# Copyright 2007 Mikael Lind.

import sys

class UnitSpec:
    def __init__(self, name):
        self.name = name
        self.speed = 0.0
        self.size = (1, 1)

class Unit:
    _keys = iter(xrange(1, sys.maxint))

    def __init__(self, spec):
        self.spec = spec
        self.key = Unit._keys.next()
        self.pos = (0, 0)
        self.locked_cells = set()

    def _get_speed(self): return self.spec.speed
    def _get_size(self): return self.spec.size

    speed = property(_get_speed)
    size = property(_get_size)
