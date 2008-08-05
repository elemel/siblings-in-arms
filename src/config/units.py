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


from Unit import Unit


class Creature(Unit):
    speed = 3.0
    damage = 1.0


class Hero(Creature):
    pass


class Monk(Hero):
    damage = 0.1
    attack_time = 0.3


class Ranger(Hero):
    speed = 4.0
    damage = 0.3
    max_range = 5.0


class Warrior(Hero):
    damage = 0.4
    max_health = 1.2


class Thief(Hero):
    damage = 0.2
    max_health = 0.8


class Knight(Hero):
    speed = 5.0
    damage = 0.3
    max_health = 1.5


class Priest(Hero):
    damage = 0.2


class Wizard(Hero):
    speed = 2.0
    damage = 0.5
    attack_time = 2.0
    max_health = 0.6


class Minion(Creature):
    size = 3, 3
    large = True


class Golem(Minion):
    damage = 0.5
    max_health = 5.0


class Building(Unit):
    max_health = 10.0
    size = 3, 3
    large = True


class Factory(Building):
    pass


class Support(Building):
    pass


class Tavern(Factory):
    pass


class Farm(Building):
    pass


class Tower(Building):
    pass


class ArcheryRange(Support):
    pass


class Barracks(Support):
    pass


class Temple(Support):
    pass


class Inn(Factory):
    pass


class GamblingDen(Support):
    pass


class Laboratory(Support):
    pass


class Stables(Support):
    pass


class Hall(Factory):
    pass
