# Copyright 2007 Mikael Lind.

import time, sys, random
from collections import deque
from GameEngine import GameEngine, tavern_spec, warrior_spec
from Unit import Unit
from Task import WaypointTask
from FrameCounter import FrameCounter

try:
    import gui
except ImportError, e:
    print "Error when importing GUI:", e
    gui = None

MIN_TIME_STEP = 0.01
MAX_TIME_STEP = 0.1

def random_pos(min_p, max_p):
    min_x, min_y = min_p
    max_x, max_y = max_p
    return (random.randint(min_x, max_x), random.randint(min_y, max_y))

def main():
    headless = ("--headless" in sys.argv)
    if not headless and gui == None:
        print ("No GUI available. Specify the --headless option for a test "
               "run in text mode.")
        sys.exit(1)
        
    game = GameEngine()
    min_p, max_p = (2, 2), (18, 16)
    game.add_unit(Unit(tavern_spec), random_pos(min_p, max_p))

    if headless:
        for i in xrange(100):
            unit = Unit(warrior_spec)
            for i in xrange(3):
                unit.add_task(WaypointTask(random_pos(min_p, max_p)))
            game.add_unit(unit, random_pos(min_p, max_p))
    
    old_time = time.time()
    frame_counter = FrameCounter()
    last_fps_time = old_time
    while True:
        new_time = time.time()
        dt = new_time - old_time
        if dt >= MIN_TIME_STEP:
            frame_counter.tick(dt)
            if dt > MAX_TIME_STEP:
                print "Skipping %d frame(s)." % int(dt / MAX_TIME_STEP)
                dt = MAX_TIME_STEP
            old_time = new_time
            game.update(dt)

            if headless:
                if new_time - last_fps_time >= 1.0:
                    last_fps_time = new_time
                    print "FPS:", frame_counter.fps
            else:
                gui.update(game, frame_counter.fps)
        else:
            time.sleep(MIN_TIME_STEP - dt)

if __name__ == "__main__":
    main()
