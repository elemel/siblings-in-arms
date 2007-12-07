# Copyright 2007 Mikael Lind.

class HitTask:
    def __init__(self, target):
        self.target = target

    def run(self, facade):
        time = 0.0
        while True:
            time += facade.dt
            if time >= facade.actor.preattack_time:
                break
            yield 0.0

        self.target.health -= facade.actor.damage
        yield 0.0

        time = 0.0
        while True:
            time += facade.dt
            if time >= facade.actor.postattack_time:
                break
            yield 0.0
