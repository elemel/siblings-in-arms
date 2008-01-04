# Copyright 2007 Mikael Lind.

import config
from Unit import Unit

class UnitManager:
    def __init__(self):
        self._specs = {}
        self._units = {}
        for spec in config.unit_specs:
            self._specs[spec.name] = spec

    def add_unit_spec(self, spec):
        self._specs[spec.name] = spec

    def remove_unit_spec(self, spec):
        del self._specs[spec.name]

    def find_unit_spec(self, name):
        return self._unit_specs.get(name, None)

    def get_unit_specs(self):
        return self._specs.itervalues()

    def add_unit(self, unit):
        self._units[unit.key] = unit

    def remove_unit(self, unit):
        del self._units[unit.key]

    def find_unit(self, key):
        return self._units.get(key, None)

    def get_build_time(self, name):
        return 0.3

    def create_unit(self, name, player):
        return Unit(self._specs[name], player)
