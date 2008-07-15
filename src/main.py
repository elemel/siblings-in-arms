# Copyright (c) 2007 Mikael Lind
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import time, sys, random
from collections import deque
from GameEngine import GameEngine
from Unit import Hero, Tavern, Warrior
from Task import MoveTask
from FrameCounter import FrameCounter


MIN_TIME_STEP = 0.01
MAX_TIME_STEP = 0.1


def random_pos(min_p, max_p):
    min_x, min_y = min_p
    max_x, max_y = max_p
    return (random.randint(min_x, max_x), random.randint(min_y, max_y))


def main():
    headless = ('-H' in sys.argv or '--headless' in sys.argv)
    if not headless:
        try:
            import gui
        except ImportError, e:
            print 'Error when importing GUI:', e
            print 'Specify the --headless option for a test run in text mode.'
            sys.exit(1)
        
    game_engine = GameEngine()
    game_engine.add_unit(Tavern('cyan'), (5, 14))
    game_engine.add_unit(Tavern('yellow'), (13, 5))

    if True or headless:
        min_p, max_p = (1, 2), (16, 16)
        colors = 'cyan', 'yellow'
        hero_types = [Warrior] # Hero.__subclasses__()
        for i in xrange(50):
            hero = random.choice(hero_types)(random.choice(colors))
            game_engine.add_unit(hero, random_pos(min_p, max_p))
    
    old_time = time.time()
    frame_counter = FrameCounter()
    last_fps_time = old_time
    while True:
        new_time = time.time()
        dt = new_time - old_time
        if dt >= MIN_TIME_STEP:
            frame_counter.tick(dt)
            if dt > MAX_TIME_STEP:
                print 'Skipping %d frame(s).' % int(dt / MAX_TIME_STEP)
                dt = MAX_TIME_STEP
            old_time = new_time
            game_engine.update(dt)

            if headless:
                if new_time - last_fps_time >= 1.0:
                    last_fps_time = new_time
                    print ('Running at %d frame(s) per second.'
                           % frame_counter.fps)
            else:
                gui.update(game_engine, frame_counter.fps)
        else:
            time.sleep(MIN_TIME_STEP - dt)


if __name__ == '__main__':
    main()
