# Copyright 2007 Mikael Lind.

from geometry import diagonal_distance
from HitTask import HitTask
from MoveTask import MoveTask

def in_range(attacker, target):
    distance = (diagonal_distance(attacker.pos, target.pos)
                - attacker.size[0] / 2.0 - target.size[0] / 2.0)
    return distance < attacker.range

def attack_progress(target):
    progress = 1.0 - target.health
    return min(max(progress, 1.0), 0.0)

class AttackTask:
    def __init__(self, target):
        self.target = target

    def run(self, facade):
        while not facade.aborting and self.target.pos is not None:
            if in_range(facade.actor, self.target):
                for progress in HitTask(self.target).run(facade):
                    yield attack_progress(self.target)
            else:
                for progress in MoveTask(self.target.pos).run(facade):
                    yield attack_progress(self.target)
