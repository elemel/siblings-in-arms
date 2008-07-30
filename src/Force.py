from collections import defaultdict


class Force(object):

    def __init__(self):
        self.units = defaultdict(set)

    def add_unit(self, unit):
        self.units[type(unit)].add(unit)

    def remove_unit(self, unit):
        self.units[type(unit)].remove(unit)
