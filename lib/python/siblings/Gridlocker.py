# Copyright 2007 Mikael Lind.

class Gridlocker:
    def __init__(self):
        self._locks = {}
        self._units = {}

    def lock(self, cell_key, unit):
        if cell_key in self._locks:
            raise RuntimeError("cell %s is already locked" % (cell_key,))
        self._locks[cell_key] = unit
        if unit.key not in self._units:
            self._units[unit.key] = set()
        self._units[unit.key].add(cell_key)
        print "%s locked cell %s." % (unit, cell_key)

    def unlock(self, cell_key):
        unit = self._locks.pop(cell_key)
        self._units[unit.key].remove(cell_key)
        if not self._units[unit.key]:
            del self._units[unit.key]
        print "%s unlocked cell %s." % (unit, cell_key)

    def locked(self, cell_key):
        return cell_key in self._locks
