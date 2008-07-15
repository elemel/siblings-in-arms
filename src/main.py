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


TIME_STEP = 0.02


def random_pos(min_p, max_p):
    min_x, min_y = min_p
    max_x, max_y = max_p
    return random.uniform(min_x, max_x), random.uniform(min_y, max_y)


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
    
    next_time = time.time()
    while True:
        current_time = time.time()
        if next_time <= current_time:
            while next_time <= current_time:
                next_time += TIME_STEP
                game_engine.update(TIME_STEP)
            if not headless:
                gui.update(game_engine)
        else:
            time.sleep(next_time - current_time)


if __name__ == '__main__':
    main()
