# Copyright 2007 Mikael Lind.

from Unit import Unit, UnitSpec

knight_spec = UnitSpec("knight")
knight_spec.speed = 7.0
knight_spec.damage = 0.3

monk_spec = UnitSpec("monk")
monk_spec.speed = 5.0
monk_spec.damage = 0.1

priest_spec = UnitSpec("priest")
priest_spec.speed = 5.0
priest_spec.damage = 0.2

ranger_spec = UnitSpec("ranger")
ranger_spec.speed = 5.0
ranger_spec.damage = 0.2

tavern_spec = UnitSpec("tavern")
tavern_spec.speed = 0.0
tavern_spec.size = (3, 3)

thief_spec = UnitSpec("thief")
thief_spec.speed = 5.0
thief_spec.damage = 0.2

warrior_spec = UnitSpec("warrior")
warrior_spec.speed = 5.0
warrior_spec.damage = 0.3

wizard_spec = UnitSpec("wizard")
wizard_spec.speed = 3.0
wizard_spec.damage = 0.5

unit_specs = {}
for spec in (knight_spec, monk_spec, priest_spec, ranger_spec, tavern_spec,
             thief_spec, warrior_spec, wizard_spec):
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
