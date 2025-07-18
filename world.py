from settings import *

class World: 
    def __init__(self, eng):
        self.eng = eng
        self.map = {}
        self.test_init()
        self.c = 0

    def init(self):
        pass

    def test_init(self):
        for c in range(COLS):
            tile = Tile(CS, CS, c, ROWS-1, BROWN_P)
            self.map[(c, ROWS-1)] = tile
        for r in range(ROWS):
            tile = Tile(CS, CS, COLS-1, r, BROWN_P)
            self.map[(COLS-1,r)] = tile

    def update(self, dt):
        pass

    def render(self, surf, dt):
        self.update(dt)
        for c in range(ROWS): 
            for r in range(COLS):
                if (c,r) in self.map:
                    tile = self.map[(c,r)]
                    tile.render(surf)

    def get_nearby_rects(self, pos):
        rects = []
        p = [int(pos[0]//CS), int(pos[1]//CS)]
        for offset in SURROUND_POS:
            key = (int(p[0] + offset[0]), int(p[1] + offset[1]))
            if key in self.map:
                rects.append(pg.Rect(key[0]*CS,key[1]*CS, CS, CS))
        return rects

class Tile:
    def __init__(self, h, w, c, r, color):
        self.size = [w, h]
        self.c = c 
        self.r = r
        self.pos = [self.c * CS, self.r * CS]
        self.color = color

    def update(self):
        pass

    def render(self, surf):
        self.update()
        pg.draw.rect(surf, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))  

    def rect(self):
        return pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def __repr__(self):
        return f'tile: COL: {self.c} ROW: {self.r} pos: {self.pos}'


