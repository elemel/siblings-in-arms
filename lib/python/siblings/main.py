# Copyright 2007 Mikael Lind.

import time, sys, random
from collections import deque
from GameEngine import GameEngine
from Unit import Unit, UnitSpec
from Task import WaypointTask

try:
    import gui
except ImportError, e:
    print "Error when importing UI:", e
    gui = None

MIN_TIME_STEP = 0.01
MAX_TIME_STEP = 0.1

tavern_spec = UnitSpec("tavern")
tavern_spec.speed = 0.0
tavern_spec.size = (3, 3)

warrior_spec = UnitSpec("warrior")
warrior_spec.speed = 5.0

def random_pos(min_p, max_p):
    min_x, min_y = min_p
    max_x, max_y = max_p
    return (random.randint(min_x, max_x), random.randint(min_y, max_y))

def main():
    game = GameEngine()
    min_p, max_p = (2, 2), (14, 11)
    game.add_unit(Unit(tavern_spec), random_pos(min_p, max_p))
    for i in xrange(20):
        game.add_unit(Unit(warrior_spec), random_pos(min_p, max_p))

    if gui is None:
        unit = Unit(warrior_spec)
        unit.add_task(WaypointTask((1, 1)))
        unit.add_task(WaypointTask((9, 9)))
        game.add_unit(unit, random_pos(min_p, max_p))
    
    old_time = time.time()
    while True:
        new_time = time.time()
        dt = new_time - old_time
        if dt >= MIN_TIME_STEP:
            if dt > MAX_TIME_STEP:
                print "Skipping %d frame(s)." % int(dt / MAX_TIME_STEP)
                dt = MAX_TIME_STEP
            old_time = new_time
            game.update(dt)
            if gui is not None:
                gui.update(game)

if __name__ == "__main__":
    main()
