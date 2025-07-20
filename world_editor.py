from settings import * 
import json 

# ---------------------- WorldEditor -------------------- #
'''
    map = {
        (2, 2):
           -1: Tile 
            0: Tile 
            1: Tile 
    }
'''

class WorldEditor:
    def __init__(self, eng) -> None:
        self.eng = eng 
        self.map = {} 

    def render(self, surf):
        for c in range(COLS):
            for r in range(ROWS):
                if (c,r) in self.map:
                    for layer in self.map[(c, r)]:
                        self.map[(c, r)][layer].render(surf)
                        

    def update(self):
        return
    
    def place_tile(self, tile_data):
        size = tile_data['size']
        grid_pos = tile_data['grid_pos']
        color = tile_data['color']
        layer = tile_data['layer']
        type = tile_data['type']
        id = tile_data['id']
        hitable = tile_data['hitable']
        if (grid_pos[0], grid_pos[1]) not in self.map:
            self.map[(grid_pos[0], grid_pos[1])] = { 
                layer: Tile(size=size, grid_pos=grid_pos, color=color, layer=layer, type=type, id=id, hitable=hitable)
            }
        else:
            if layer not in self.map[(grid_pos[0], grid_pos[1])]:
                self.map[(grid_pos[0], grid_pos[1])] = { 
                    layer: Tile(size=size, grid_pos=grid_pos, color=color, layer=layer, type=type, id=id, hitable=hitable)
                }

    def remove_tile(self, grid_pos, layer):
        if (grid_pos[0], grid_pos[1]) in self.map:
            if layer in self.map[(grid_pos[0], grid_pos[1])]:
                del self.map[(grid_pos[0], grid_pos[1])]
            else:
                print('layer not found')
        else:
            print('pos not found')

    def json_format(self):
        pass

# ---------------------- TILE -------------------- #

# type / category / id / layer 
# decor / foliage / tree / -1
# decor / furniture / chair / 0 
# tile : { size: [16, 16], map_pos: [col, row], color : WHITE, layer: 0, type: 'hazard', id: 0 }
# tile : { size: [16, 16], map_pos: [col, row], color : WHITE, layer: 0, type: 'solid',  id: 0 }

class Tile:
    def __init__(self, size, grid_pos, color, layer, type, id, hitable):
        self.size = size.copy()
        self.grid_pos = grid_pos.copy()
        self.pos = [self.grid_pos[0] * CS, self.grid_pos[1] * CS]
        self.color = color
        self.layer = layer
        self.type = type
        self.id = id
        self.hitable = hitable

    def update(self):
        return

    def render(self, surf):
        self.update()
        pg.draw.rect(surf, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))

    def json_format(self):
        return { 
                'size': [self.size[0], self.size[1]], 
                'grid_pos': [self.grid_pos[0], self.grid_pos[1]], 
                'color': self.color,
                'layer': self.layer, 
                'type': self.type,
                'id': self.id
            }

# ---------------------- JSON -------------------- #

def save_map(path, map):
    pass 

def load_map(path):
    pass

def test_save(object):
    pth = 'maps/test_tile.json'
    fl = open(pth, 'w')
    json.dump(object, fl)
    fl.close()

def test_load_json():
    pth = 'maps/test_tile.json'
    fl = open(pth, 'r')
    map_data = json.load(fl)
    fl.close()
    print(map_data)
    

