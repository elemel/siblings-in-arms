# Copyright 2007 Mikael Lind.

from geometry import diagonal_distance
from MoveTask import MoveTask

def in_range(attacker, target):
    distance = (diagonal_distance(attacker.pos, target.pos)
                - attacker.size[0] / 2.0 - target.size[0] / 2.0)
    return distance < attacker.range

class AttackTask:
    def __init__(self, target):
        self.target = target

    def run(self, facade):
        while not facade.aborting and self.target.health > 0:
            if in_range(facade.actor, self.target):
                self.target.health -= facade.actor.damage * facade.dt
                yield 1.0 - min(max(self.target.health, 1.0), 0.0)
            else:
                for progress in MoveTask(self.target.pos).run(facade):
                    yield progress
