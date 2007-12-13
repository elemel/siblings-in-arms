# Copyright 2007 Mikael Lind.

class UnitSpec:
    def __init__(self, name):
        self.name = name
        self.speed = None
        self.size = (1, 1)
        self.damage = None
        self.min_range = 0.0
        self.max_range = 1.0
        self.preattack_time = 0.5
        self.postattack_time = 0.5
        self.max_health = 1.0

    def _set_attack_time(self, time):
        self.preattack_time = time / 2.0
        self.postattack_time = time / 2.0

    def _get_attack_time(self):
        return self.preattack_time + self.postattack_time

    attack_time = property(_set_attack_time, _get_attack_time)
