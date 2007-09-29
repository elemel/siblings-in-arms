def generate_num():
    num = 1
    while True:
        yield num
        num = num + 1

class Unit(object):
    _num_generator = generate_num()

    def __init__(self):
        self._num = self._num_generator.next()
        self._pos = (0.0, 0.0)

    def get_num(self):
        return self._num

    num = property(get_num)
    
    def get_pos(self):
        return self._pos

    def set_pos(self, pos):
        self._pos = pos
        
    pos = property(get_pos, set_pos)
