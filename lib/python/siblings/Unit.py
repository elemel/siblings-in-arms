# Copyright 2007 Mikael Lind.

import sys

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
    def _get_min_range(self): return self._spec.min_range
    def _get_max_range(self): return self._spec.max_range
    def _get_preattack_time(self): return self._spec.preattack_time
    def _get_postattack_time(self): return self._spec.postattack_time

    spec = property(_get_spec)
    key = property(_get_key)
    speed = property(_get_speed)
    size = property(_get_size)
    damage = property(_get_damage)
    min_range = property(_get_min_range)
    max_range = property(_get_max_range)
    preattack_time = property(_get_preattack_time)
    postattack_time = property(_get_postattack_time)

    def __str__(self):
        return "%s %s #%d" % (self.player.capitalize(),
                              self._spec.name.capitalize(), self._key)
