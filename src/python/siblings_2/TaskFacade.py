# Copyright 2007 Mikael Lind.

class TaskFacade:
    def __init__(self, unit):
        self.unit = unit
        self.dt = 0.0
        self.game = None

    def find_path(self, waypoint):
        return self.game.find_path(self.unit, waypoint)

    def reserve_cell(self, pos):
        if self.game.reserve_cell(self.unit, pos):
            self.unit.cells.add(pos)
            return True
        else:
            return False

    def release_cell(self, pos):
        if pos in self.unit.cells:
            self.unit.cells.remove(pos)
            self.game.release_cell(self.unit, pos)
