from Vector2 import Vector2

def generate_num():
    num = 1
    while True:
        yield num
        num = num + 1

class Unit(object):
    _num_generator = generate_num()

    def __init__(self):
        self._num = self._num_generator.next()
        self._pos = Vector2()
        self._velocity = Vector2()

    def get_num(self):
        return self._num

    num = property(get_num)
    
    def get_pos(self):
        return self._pos

    def set_pos(self, pos):
        self._pos = pos
        
    pos = property(get_pos, set_pos)

    def get_velocity(self):
        return self._velocity

    def set_velocity(self, velocity):
        self._velocity = velocity

    velocity = property(get_velocity, set_velocity)

    def get_max_velocity(self):
        return self._max_velocity

    max_velocity = property(get_max_velocity)
