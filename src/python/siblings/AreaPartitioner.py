from Vector2 import Vector2

class AreaPartitioner(object):
    DEFAULT_TILE_SIZE = 5.0

    def __init__(self, tile_size = None):
        if tile_size is None:
            tile_size = self.DEFAULT_TILE_SIZE
        self._tile_size = tile_size
        self._tiles = {}
        self._units = {}

    def _get_tile_key(self, pos):
        return int(pos.x / self._tile_size), int(pos.y / self._tile_size)
        
    def add_unit(self, unit):
        tile_key = self._get_tile_key(unit.pos)
        self._units[unit.num] = tile_key
        
        tile = self._tiles.get(tile_key, None)
        if tile == None:
            tile = []
            self._tiles[tile_key] = tile
        tile.append(unit)
        
    def remove_unit(self, unit):
        tile_key = self._units.pop(unit.num)
        
        tile = self._tiles[tile_key]
        tile.remove(unit)
        if len(tile) == 0:
            del self._tiles[tile_key]

    def _log_tile_move(self, unit, old_key, new_key):
        print ("Moved unit #%d from tile %s to tile %s, "
               "which now contains %d unit(s)."
               % (unit.num, old_key, new_key, len(self._tiles[new_key])))

    def update_unit(self, unit):
        old_key = self._units[unit.num]
        new_key = self._get_tile_key(unit.pos)
        if new_key != old_key:
            self.remove_unit(unit)
            self.add_unit(unit)
            # self._log_tile_move(unit, old_key, new_key)

    def _get_min_and_max_keys(self, shape):
        bounding_box = shape.bounding_box
        min_key = self._get_tile_key(bounding_box.min_point)
        max_key = self._get_tile_key(bounding_box.max_point)
        return min_key, max_key

    def _search_tile(self, key, shape, found):
        tile = self._tiles.get(key, None)
        if tile != None:
            for unit in tile:
                if shape.contains_point(unit.pos):
                    found.append(unit)

    def find_units(self, shape):
        found_units = []
        min_key, max_key = self._get_min_and_max_keys(shape)
        for x_index in range(min_key[0], max_key[0] + 1):
            for y_index in range(min_key[1], max_key[1] + 1):
                key = x_index, y_index
                self._search_tile(key, shape, found_units)
        return found_units
