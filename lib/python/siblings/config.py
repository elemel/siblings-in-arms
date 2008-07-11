from UnitSpec import UnitSpec

monk_spec = UnitSpec("monk")
monk_spec.speed = 4.0
monk_spec.damage = 0.1

warrior_spec = UnitSpec("warrior")
warrior_spec.speed = 4.0
warrior_spec.damage = 0.4
warrior_spec.max_health = 1.2

knight_spec = UnitSpec("knight")
knight_spec.speed = 6.0
knight_spec.damage = 0.3
knight_spec.max_health = 1.5

ranger_spec = UnitSpec("ranger")
ranger_spec.speed = 5.0
ranger_spec.damage = 0.3

rogue_spec = UnitSpec("rogue")
rogue_spec.speed = 4.0
rogue_spec.damage = 0.2
rogue_spec.max_health = 0.8

priest_spec = UnitSpec("priest")
priest_spec.speed = 4.0
priest_spec.damage = 0.2

wizard_spec = UnitSpec("wizard")
wizard_spec.speed = 3.0
wizard_spec.damage = 0.5
wizard_spec.preattack_time = 1.0
wizard_spec.postattack_time = 0.5
wizard_spec.max_health = 0.6

tavern_spec = UnitSpec("tavern")
tavern_spec.speed = 0.0
tavern_spec.size = (3, 3)
tavern_spec.max_health = 10.0

unit_specs = [monk_spec, warrior_spec, ranger_spec, knight_spec, rogue_spec,
              priest_spec, wizard_spec, tavern_spec]
