# Copyright 2007 Mikael Lind.

from geometry import diagonal_distance, vector_add, vector_mul

def interpolate_pos(old_p, new_p, progress):
    return vector_add(vector_mul(old_p, 1 - progress),
                      vector_mul(new_p, progress))

class StepTask:
    def __init__(self, pos):
        self.pos = pos

    def run(self, facade):
        old_pos = facade.actor.pos
        distance = diagonal_distance(old_pos, self.pos)
        progress = 0.0
        while True:
            progress += facade.dt * facade.actor.speed / distance
            if progress >= 1.0:
                break
            facade.actor.pos = interpolate_pos(old_pos, self.pos, progress)
            yield progress
        facade.actor.pos = self.pos
