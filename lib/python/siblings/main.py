# Copyright 2007 Mikael Lind.

import time, sys, random
from a_star_search import a_star_search, grid_neighbors, diagonal_distance
from collections import deque
try:
    import ui
    from ui import QuitEvent, MoveEvent, SelectEvent
except ImportError, e:
    print "Error when importing UI:", e
    ui = None
from GameEngine import GameEngine
from Unit import Unit
from Task import WaypointTask

MIN_TIME_STEP = 0.01
MAX_TIME_STEP = 0.1

def main():
    game = GameEngine()
    for i in xrange(20):
        game.add_unit(Unit(), (random.randint(1, 14), random.randint(1, 14)))

    if ui is None:
        unit = Unit()
        unit.add_task(WaypointTask((1, 1)))
        unit.add_task(WaypointTask((9, 9)))
        game.add_unit(unit, (4, 8))
    
    old_time = time.time()
    selected = None
    while True:
        new_time = time.time()
        dt = new_time - old_time
        if dt >= MIN_TIME_STEP:
            if dt > MAX_TIME_STEP:
                print "Skipping %d frame(s)." % int(dt / MAX_TIME_STEP)
                dt = MAX_TIME_STEP
            old_time = new_time
            if ui is not None:
                for e in ui.poll_events(game):
                    if isinstance(e, SelectEvent):
                        selected = e.unit
                        print "Selected unit #%d." % selected.key
                    elif isinstance(e, MoveEvent):
                        if selected is not None:
                            x, y = e.pos
                            pos = (int(round(x)), int(round(y)))
                            selected.add_task(WaypointTask(pos))
                            print ("Set waypoint %s for unit #%d."
                                   % (pos, selected.key))
                    elif isinstance(e, QuitEvent):
                        sys.exit(0)
            game.update(dt)
            if ui is not None:
                ui.update_screen(game)

if __name__ == "__main__":
    main()
