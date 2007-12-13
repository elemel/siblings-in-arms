# Copyright 2007 Mikael Lind.

from Unit import Unit, UnitSpec

knight_spec = UnitSpec("knight")
knight_spec.speed = 6.0
knight_spec.damage = 0.3

monk_spec = UnitSpec("monk")
monk_spec.speed = 4.0
monk_spec.damage = 0.1

priest_spec = UnitSpec("priest")
priest_spec.speed = 4.0
priest_spec.damage = 0.2

ranger_spec = UnitSpec("ranger")
ranger_spec.speed = 5.0
ranger_spec.damage = 0.3

rogue_spec = UnitSpec("rogue")
rogue_spec.speed = 4.0
rogue_spec.damage = 0.2

tavern_spec = UnitSpec("tavern")
tavern_spec.speed = 0.0
tavern_spec.size = (3, 3)

warrior_spec = UnitSpec("warrior")
warrior_spec.speed = 4.0
warrior_spec.damage = 0.4

wizard_spec = UnitSpec("wizard")
wizard_spec.speed = 3.0
wizard_spec.damage = 0.5
wizard_spec.preattack_time = 1.0
wizard_spec.postattack_time = 0.5

class UnitManager:
    def __init__(self):
        self._specs = {}
        self._units = {}

        for spec in (knight_spec, monk_spec, priest_spec, ranger_spec,
                     rogue_spec, tavern_spec, warrior_spec, wizard_spec):
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
