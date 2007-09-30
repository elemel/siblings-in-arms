TIME_STEP = 0.01

class GameEngine:
    def __init__(self, time):
        self._units = []
        self._old_time = time
        self._last_update = time
        
    def add_unit(self, unit, pos = None):
        if pos:
            unit.pos = pos
        self._units.append(unit)

    def get_units(self):
        return iter(self._units)

    units = property(get_units)

    def _update_unit(self, unit, dt):
        unit.pos = unit.pos + unit.velocity * dt

    def _update_step(self, dt):
        for unit in self._units:
            self._update_unit(unit, dt)

    def update(self, time):
        while self._last_update + TIME_STEP < time:
            self._update_step(TIME_STEP)
            self._last_update = self._last_update + TIME_STEP
