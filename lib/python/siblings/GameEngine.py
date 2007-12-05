# Copyright 2007 Mikael Lind.

import time, sys
from Unit import Unit, UnitSpec
from TaskFacade import TaskFacade
from Pathfinder import Pathfinder
from Gridlocker import Gridlocker
from Taskmaster import Taskmaster
from UnitManager import UnitManager

class GameEngine:
    def __init__(self):
        self.task_facade = TaskFacade(self)
        self.taskmaster = Taskmaster(self.task_facade)
        self.gridlocker = Gridlocker()
        self.pathfinder = Pathfinder(self.gridlocker)
        self.unit_manager = UnitManager(self.gridlocker)
        
    def update(self, dt):
        self.pathfinder.update()
        self.taskmaster.update(dt)
