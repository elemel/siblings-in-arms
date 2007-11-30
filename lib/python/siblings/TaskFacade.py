# Copyright 2007 Mikael Lind.

class TaskFacade:
    def __init__(self, unit):
        self.unit = unit
        self.dt = 0.0
        self.game = None

    def find_path(self, waypoint, callback):
        self.game.find_path(self.unit, waypoint, callback)

    def lock_cell(self, pos):
        return self.game.lock_cell(self.unit, pos)

    def unlock_cell(self, pos):
        self.game.unlock_cell(self.unit, pos)
