from __future__ import division
from AreaPartitioner import AreaPartitioner
from Circle2 import Circle2
from Vector2 import Vector2

class GameEngine:
    DEFAULT_TIME_STEP = 0.02 # 50 FPS

    def __init__(self, start_time, time_step = None):
        if time_step == None:
            time_step = self.DEFAULT_TIME_STEP
        self._last_update = start_time
        self._time_step = time_step
        
        self._units = []
        self._partitioner = AreaPartitioner()
        
    def add_unit(self, unit):
        self._units.append(unit)
        self._partitioner.add_unit(unit)

    def get_units(self):
        return iter(self._units)

    units = property(get_units)

    def _update_unit(self, unit, dt):
        found_units = self.find_units(Circle2(unit.pos, 5.0))
        found_units.remove(unit)

        if abs(unit.velocity) == 0.0:
            acceleration = Vector2()
        else:
            acceleration = -3.0 * unit.velocity / abs(unit.velocity)

        for other in found_units:
            dist = abs(unit.pos - other.pos)
            if dist <= 2.0:
                acceleration += 10.0 * (unit.pos - other.pos) / (dist * dist)
        if abs(acceleration) > unit.max_acceleration:
            acceleration = (unit.max_acceleration
                            * acceleration / abs(acceleration))

        unit.velocity += acceleration * dt
        unit.pos += unit.velocity * dt
        self._partitioner.update_unit(unit)

    def _update_step(self, dt):
        for unit in self._units:
            self._update_unit(unit, dt)

    def update(self, time):
        if self._last_update + self._time_step < time:
            self._update_step(self._time_step)
            self._last_update += self._time_step
            if self._last_update + self._time_step < time:
                self._last_update = time
                print "Skipped updates."

    def find_units(self, shape):
        return self._partitioner.find_units(shape)
