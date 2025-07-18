from settings import * 

class TileEditor():
    def __init__(self) -> None:
        pg.init()
        # GAME SETTINGS 
        self.running = True
        self.font = pg.font.Font(None, 16)
        self.clock = pg.time.Clock()
        self.screen: pg.display = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf: pg.Surface = pg.Surface((WIDTH, HEIGHT))