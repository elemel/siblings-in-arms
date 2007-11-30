# Copyright 2007 Mikael Lind.

class Event:
    pass

class QuitEvent(Event):
    pass

class SelectEvent(Event):
    def __init__(self, unit):
        self.unit = unit

class MoveEvent(Event):
    def __init__(self, pos):
        self.pos = pos
