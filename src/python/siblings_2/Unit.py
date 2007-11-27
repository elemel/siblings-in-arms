# Copyright 2007 Mikael Lind.

import sys
from collections import deque
from a_star_search import diagonal_distance

IDLE = 1
REQUEST_PATH = 2
WAIT_FOR_PATH = 3
START_MOVING = 4
MOVE = 5

class Unit:
    _keys = iter(xrange(1, sys.maxint))

    def __init__(self):
        self.key = Unit._keys.next()
        self.old_pos = (0, 0)
        self.new_pos = self.old_pos
        self.state = IDLE
        self.path = deque()
        self.waypoints = deque()
        self.progress = 0
        self.cost = 1
        self.cells = set()
        self.speed = 5

    def get_pos(self):
        if self.old_pos == self.new_pos:
            return self.old_pos
        else:
            old_x, old_y = self.old_pos
            new_x, new_y = self.new_pos
            new_weight = min(float(self.progress) / self.cost, 1.0)
            x = old_x * (1 - new_weight) + new_x * new_weight
            y = old_y * (1 - new_weight) + new_y * new_weight
            return (x, y)

    pos = property(get_pos)
    
    def update(self, dt, game):
        if self.state == IDLE:
            if self.path:
                self.state = START_MOVING
            elif self.waypoints:
                self.state = REQUEST_PATH
        if self.state == REQUEST_PATH:
            self._request_path(dt, game)
        if self.state == MOVE:
            self._move(dt, game)
        if self.state == START_MOVING:
            self._start_moving(dt, game)

    def stop(self):
        self.waypoints.clear()
        self.path.clear()

    def add_waypoint(self, waypoint):
        self.waypoints.append(waypoint)

    def set_waypoint(self, waypoint):
        self.stop()
        self.add_waypoint(waypoint)

    def set_path(self, path):
        if self.state == WAIT_FOR_PATH:
            self.path = path
            self.state = IDLE

    def _request_path(self, dt, game):
        game.request_path(self, self.waypoints.popleft())
        self.state = WAIT_FOR_PATH

    def _start_moving(self, dt, game):
        pos = self.path.popleft()
        if game.reserve_cell(self, pos):
            self.cells.add(pos)
            self.new_pos = pos
            self.progress = 0
            self.cost = diagonal_distance(self.old_pos, self.new_pos)
            self.state = MOVE
        else:
            self.path.clear()
            self.state = IDLE

    def _move(self, dt, game):
        self.progress += dt * self.speed
        if self.progress >= self.cost:
            if self.old_pos in self.cells:
                game.release_cell(self, self.old_pos)
                self.cells.remove(self.old_pos)
            self.old_pos = self.new_pos
            self.state = IDLE
