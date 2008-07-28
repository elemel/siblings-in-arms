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


from __future__ import division
from itertools import izip
from math import sqrt


class Vector(object):

    def __init__(self, *args):
        self.__comps = tuple(args[0] if len(args) == 1 else args)

    def __iter__(self):
        return iter(self.__comps)

    def __getitem__(self, i):
        return self.__comps[i]

    def __add__(self, other):
        return Vector(x + y for x, y in izip(self.__comps, other))

    def __sub__(self, other):
        return Vector(x - y for x, y in izip(self.__comps, other))

    def __mul__(self, other):
        return Vector(x * other for x in self.__comps)

    __rmul__ = __mul__

    def __div__(self, other):
        return Vector(x / other for x in self.__comps)

    def __abs__(self):
        return sqrt(sum(x ** 2 for x in self.__comps))

    def __hash__(self):
        return hash(self.__comps)

    def __cmp__(self, other):
        return -cmp(other, self.__comps)
