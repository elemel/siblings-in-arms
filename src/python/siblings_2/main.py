# Copyright 2007 Mikael Lind.

import time, sys
from a_star_search import a_star_search, grid_neighbors, diagonal_distance
from collections import deque
import ui
from ui import QuitEvent, MoveEvent, SelectEvent
from GameEngine import GameEngine
from Unit import Unit
from Task import WaypointTask

MIN_TIME_STEP = 0.01
MAX_TIME_STEP = 0.1

def main():
    game = GameEngine()
    game.add_unit(Unit(), (2, 3))
    game.add_unit(Unit(), (7, 4))
    game.add_unit(Unit(), (6, 5))
    game.add_unit(Unit(), (3, 7))
    game.add_unit(Unit(), (8, 2))
    game.add_unit(Unit(), (5, 6))
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
            ui.update_screen(game)

if __name__ == "__main__":
    main()
