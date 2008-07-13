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
