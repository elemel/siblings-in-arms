class Unit(object):
    def __init__(self):
        self._pos = (0.0, 0.0)
    
    def get_pos(self):
        return self._pos

    def set_pos(self, pos):
        self._pos = pos
        
    pos = property(get_pos, set_pos)
