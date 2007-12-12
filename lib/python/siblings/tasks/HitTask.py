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

        damage_factor = facade.get_damage_factor(facade.actor, self.target)
        self.target.health -= facade.actor.damage * damage_factor
        print "%s hit %s." % (facade.actor, self.target)
        yield 0.0

        time = 0.0
        while True:
            time += facade.dt
            if time >= facade.actor.postattack_time:
                break
            yield 0.0
