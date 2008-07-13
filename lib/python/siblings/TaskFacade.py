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


from geometry import rectangle_from_center_and_size


class TaskFacade:

    def __init__(self, game_engine):
        self.__game_engine = game_engine
        self.dt = 0.0
        self.actor = None
        self.aborting = False

    def request_path(self, unit, waypoint, callback):
        self.__game_engine.request_path(unit, waypoint, callback)

    def lock_cell(self, unit, cell):
        return self.__game_engine.lock_cell(unit, cell)

    def unlock_cell(self, cell):
        self.__game_engine.unlock_cell(cell)

    def locked_cell(self, cell):
        return self.__game_engine.locked_cell(cell)

    def create_unit(self, name, player):
        return self.__game_engine.unit_manager.create_unit(name, player)

    def add_unit(self, unit, pos):
        self.__game_engine.add_unit(unit, pos)

    def set_pos(self, unit, pos):
        unit.pos = pos
        rect = rectangle_from_center_and_size(unit.pos, unit.size)
        self.__game_engine.proximity_grid[unit.key] = rect

    def request_task(self, unit, callback):
        pass

    def remove_task_request(self, unit):
        pass

    def get_damage_factor(self, attacker, defender):
        return self.__game_engine.get_damage_factor(attacker, defender)

    def cell_to_pos(self, cell):
        return self.__game_engine.grid.cell_to_pos(cell)
