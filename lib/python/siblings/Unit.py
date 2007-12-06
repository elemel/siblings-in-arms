# Copyright 2007 Mikael Lind.

import sys

class UnitSpec:
    def __init__(self, name):
        self.name = name
        self.speed = 0.0
        self.size = (1, 1)
        self.damage = 0.0

class Unit:
    _keys = iter(xrange(1, sys.maxint))

    def __init__(self, spec, player = None):
        self._spec = spec
        self._key = Unit._keys.next()
        self.player = player
        self.pos = None
        self.health = 1.0

    def _get_spec(self): return self._spec
    def _get_key(self): return self._key
    def _get_speed(self): return self._spec.speed
    def _get_size(self): return self._spec.size
    def _get_damage(self): return self._spec.damage

    spec = property(_get_spec)
    key = property(_get_key)
    speed = property(_get_speed)
    size = property(_get_size)
    damage = property(_get_damage)
