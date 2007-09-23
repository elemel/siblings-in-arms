class GameEngine:
    def __init__(self):
        self._units = []
        
    def add_unit(self, unit, pos = None):
        if pos:
            unit.pos = pos
        self._units.append(unit)

    def get_units(self):
        return self._units.__iter__()

    units = property(get_units)

    def update(self, dt):
        for unit in self._units:
            unit.update(dt)
