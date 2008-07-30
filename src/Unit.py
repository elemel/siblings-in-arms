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


from collections import deque


class Unit(object):

    speed = None
    size = 1, 1
    damage = None
    min_range = 0.0
    max_range = 0.5
    attack_time = 0.5
    max_health = 1.0
    build_time = 0.3
    large = False

    def __init__(self, color):
        self.color = color
        self.alive = True
        self.health = self.max_health
        self.task_stack = []
        self.task_queue = deque()
        self.moving = False
        self.cell = None
        self.cell_locks = set()

    def __str__(self):
        return "%s %s #%d" % (self.color.capitalize(), type(self).__name__,
                              id(self))

    def __nonzero__(self):
        return self.alive
