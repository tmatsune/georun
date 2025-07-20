from settings import * 
from utils import * 
from world_editor import * 

class TileEditor():
    def __init__(self) -> None:
        pg.init()
        # GAME SETTINGS 
        self.running = True
        self.font = pg.font.Font(None, 16)
        self.clock = pg.time.Clock()
        self.screen: pg.display = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf: pg.Surface = pg.Surface((WIDTH, HEIGHT))
        self.dt = 0
        self.tt = 0
        # INTERACTION SETTINGS
        self.mouse_pos = [0, 0]
        self.movement = [False, False, False, False]
        self.left_clicked = False
        self.remove_clicked = False
        
        # WORLD SETTINGS
        self.world_editor = WorldEditor(self)

        # OTHER 
        self.colors = [BLACK_P, BROWN_P, RED_P, OFFWHITE_P]
        self.types = ['decor', 'solid', 'hazard']

        # PLACING VARIABLES
        self.tile_color_idx = 0                     # 0 - 3
        self.tile_size = [CS, CS]                   # 
        self.tile_grid_pos = [0,0]                  # 
        self.tile_layer = 0                         # -inf - inf 
        self.tile_type = 0                          # decor, solid, hazard
        self.tile_id = 0                            # TODO 0 - 3 only for hazard 
        self.tile_hitable = True
        # Keys: change_color: [q, e], layer: [z, c], type: [f, g], id: [v, b]

        # TEST SETTINGS 
        self.test_tile = Tile(
            [CS, CS], 
            [10,10], 
            self.colors[self.tile_color_idx], 
            self.tile_layer, 
            self.types[self.tile_type],
            self.tile_id,
            self.tile_hitable
            )

    def render(self):
        self.surf.fill(BLACK)

        # world
        self.world_editor.render(self.surf)
        if self.left_clicked:
            if self.remove_clicked:
                print('remove')
                self.world_editor.remove_tile(self.tile_grid_pos, self.tile_layer)
            else:
                print('place tile')
                tile_data = {
                    'size': self.tile_size,
                    'grid_pos' : self.tile_grid_pos,
                    'color': self.colors[self.tile_color_idx], 
                    'layer': self.tile_layer,
                    'type': self.tile_type,
                    'id': self.tile_id,
                    'hitable': self.tile_hitable
                    }
                self.world_editor.place_tile(tile_data)
        
        # mouse
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_pos = [self.mouse_pos[0]//CS//SCALE, self.mouse_pos[1]//CS//SCALE]
        self.tile_grid_pos = self.mouse_pos.copy()

        # text
        text_surf_1 = text_surface(f'tile co lor: {self.tile_color_idx}', 9, False, WHITE, 'arial', False)
        self.surf.blit(text_surf_1, (4, 10))
        if self.types[self.tile_type] == 'decor':
            pass
        elif self.types[self.tile_type] == 'solid':
            pg.draw.rect(self.surf, self.colors[self.tile_color_idx], (60, 10, 12, 12))
            pg.draw.rect(self.surf, WHITE, (60, 10, 12, 12), 1)
        elif self.types[self.tile_type] == 'hazard':
            pass

        text_surf_2 = text_surface(f'tile layer: {self.tile_layer}', 9, False, WHITE, 'arial', False)
        self.surf.blit(text_surf_2, (4, 20))

        text_surf_3 = text_surface(f'tile type: {self.types[self.tile_type]}', 9, False, WHITE, 'arial', False)
        self.surf.blit(text_surf_3, (4, 30))

        text_surf_4 = text_surface(f'tile hitable: {self.tile_hitable}', 9, False, WHITE, 'arial', False)
        self.surf.blit(text_surf_4, (4, 40))

        # render screen 
        pg.display.flip()
        pg.display.update()
        self.screen.blit(pg.transform.scale(self.surf, self.screen.get_size()), (0, 0))

    def update(self):
        fps = self.clock.get_fps()
        self.dt = self.clock.tick(FPS) / 1000
        pg.display.set_caption(f"FPS: {fps:.2f}")
        self.tt += self.dt

    def change_color(self, change):
        self.tile_color_idx += change
        if self.tile_color_idx >= len(self.colors): 
            self.tile_color_idx = 0 
        if self.tile_color_idx < 0:
            self.tile_color_idx = len(self.colors) - 1

    def change_layer(self, change):
        self.tile_layer += change 

    def change_type(self, change):
        self.tile_type += change 
        if self.tile_type >= len(self.types):
            self.tile_type = 0
        if self.tile_type < 0:
            self.tile_type = len(self.types) - 1

    def change_id(self, change):
        # TODO 
        pass

    def change_hitable(self):
        self.tile_hitable = not self.tile_hitable

    def check_inputs(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.running = False
                if e.key == pg.K_a:
                    self.movement[0] = True
                if e.key == pg.K_d:
                    self.movement[1] = True
                if e.key == pg.K_w:
                    self.movement[2] = True
                if e.key == pg.K_s:
                    self.movement[3] = True
                if e.key == pg.K_r:
                    self.remove_clicked = True

                if e.key == pg.K_z: self.change_color(-1)
                if e.key == pg.K_x: self.change_color(1)
                if e.key == pg.K_c: self.change_layer(-1)
                if e.key == pg.K_v: self.change_layer(1)
                if e.key == pg.K_b: self.change_type(-1)
                if e.key == pg.K_n: self.change_type(1)
                if e.key == pg.K_m: pass 

                if e.key == pg.K_t:
                    test_save(self.test_tile.json_format())
                if e.key == pg.K_y:
                    test_load_json()

            if e.type == pg.KEYUP:
                if e.key == pg.K_a:
                    self.movement[0] = False
                if e.key == pg.K_d:
                    self.movement[1] = False
                if e.key == pg.K_w:
                    self.movement[2] = False
                if e.key == pg.K_s:
                    self.movement[3] = False
                if e.key == pg.K_r:
                    self.remove_clicked = True

            if e.type == pg.MOUSEBUTTONDOWN:
                self.left_clicked = True
            if e.type == pg.MOUSEBUTTONUP:
                self.left_clicked = False

    def run(self):
        while self.running:
            self.check_inputs()
            self.update()
            self.render()

def main():
    gm = TileEditor()
    gm.run()

if __name__ == "__main__":
    main()
