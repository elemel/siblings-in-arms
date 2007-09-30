from AreaPartitioner import AreaPartitioner

DEFAULT_TIME_STEP = 0.01

class GameEngine:
    def __init__(self, start_time, time_step = DEFAULT_TIME_STEP):
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
        unit.pos = unit.pos + unit.velocity * dt
        self._partitioner.update_unit(unit)

    def _update_step(self, dt):
        for unit in self._units:
            self._update_unit(unit, dt)

    def update(self, time):
        while self._last_update + self._time_step < time:
            self._update_step(self._time_step)
            self._last_update = self._last_update + self._time_step

    def find_units(self, center, radius):
        return self._partitioner.find_units(center, radius)
