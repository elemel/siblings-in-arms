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


import time
from Game import Game
from Screen import Screen
from Unit import Tavern


TIME_STEP = 0.02


def main():
    game = Game()
    game.add_unit(Tavern('cyan'), game.point_to_cell((4, 10)))
    game.add_unit(Tavern('yellow'), game.point_to_cell((12, 6)))

    screen = Screen()

    next_time = time.time()
    while True:
        current_time = time.time()
        if next_time <= current_time:
            while next_time <= current_time:
                next_time += TIME_STEP
                game.update(TIME_STEP)
            screen.update(game)
        else:
            time.sleep(next_time - current_time)


if __name__ == '__main__':
    main()
