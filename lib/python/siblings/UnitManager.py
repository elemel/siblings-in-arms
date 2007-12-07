# Copyright 2007 Mikael Lind.

from Unit import Unit, UnitSpec

monk_spec = UnitSpec("monk")
monk_spec.speed = 4.0
monk_spec.damage = 0.1

tavern_spec = UnitSpec("tavern")
tavern_spec.speed = 0.0
tavern_spec.size = (3, 3)

warrior_spec = UnitSpec("warrior")
warrior_spec.speed = 5.0
warrior_spec.damage = 0.3

unit_specs = {}
for spec in monk_spec, tavern_spec, warrior_spec:
    unit_specs[spec.name] = spec

class UnitManager:
    def __init__(self):
        self._units = {}
        
    def add_unit(self, unit):
        self._units[unit.key] = unit

    def remove_unit(self, unit):
        del self._units[unit.key]

    def get_build_time(self, name):
        return 0.3

    def create_unit(self, name, player):
        return Unit(unit_specs[name], player)
