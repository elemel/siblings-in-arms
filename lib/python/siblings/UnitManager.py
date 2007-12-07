# Copyright 2007 Mikael Lind.

from Unit import Unit, UnitSpec

tavern_spec = UnitSpec("tavern")
tavern_spec.speed = 0.0
tavern_spec.size = (3, 3)

warrior_spec = UnitSpec("warrior")
warrior_spec.speed = 5.0
warrior_spec.damage = 1.0

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
        return Unit(warrior_spec, player)
