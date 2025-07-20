from settings import *
from utils import * 
from entities import *
from world import * 
from particles import Particle, FloatingParticle, Spark, spark_collision 

class GameEngine:
    def __init__(self):
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
        self.mous_pos = [0, 0]
        self.movement = [False, False, False, False]
        # WORLD SETTINGS 
        self.world = World(self)
        # PLAYER 
        self.player = Player(self)   
        # PARTICLES
        self.particles = []
        self.floating_particles = []
        self.sparks = []
        # TEST VARS 
        self.test_pos = [120, 120]
        self.test_angle = -90
        self.test_l = 0.2
        self.speed = 2 
        self.scale = 2 

    def render(self):
        self.surf.fill(OFFWHITE_P)
        
        # PARTICLES 
        for p in self.particles:
            p.render(self.surf, self.dt)
            if p.done: 
                self.particles.remove(p)
        for p in self.floating_particles:
            p.render(self.surf, self.dt)
            if p.done:
                self.floating_particles.remove(p)
        for s in self.sparks:
            s.render(self.surf, self.dt)
            if s.done: 
                self.sparks.remove(s)

        # PLAYER
        self.player.render(self.surf, self.movement, self.dt)

        # ---- TEST ---- #
        self.test_func(self.surf)
        # -------------- #

        # WORLD 
        self.world.render(self.surf, self.dt)

        pg.display.flip()
        self.screen.blit(pg.transform.scale(self.surf, self.screen.get_size()), (0, 0))

    def update(self):
        fps = self.clock.get_fps()
        self.dt = self.clock.tick(FPS) / 1000
        pg.display.set_caption(f"FPS: {fps:.2f}")
        self.tt += self.dt

    def test_func(self, surf):

        pos = self.test_pos.copy()
        angle = self.test_angle 
        angle = math.radians(angle) 
        steepness = 40
        steepness = math.radians(steepness)
        speed = self.speed
        scale = 1
        #self.speed *= 0.98
        if self.speed < 0.2:
            self.test_pos = [1000,1000]

        start_x = pos[0] + (.1 * speed * scale * math.cos(angle))
        start_y = pos[1] + (.1 * speed * scale * math.sin(angle))

        left_x = pos[0] +  (3 * speed * scale * math.cos(angle-steepness))
        left_y = pos[1] +  (3 * speed * scale * math.sin(angle-steepness))

        tip_x = pos[0] + (7 * speed * scale * math.cos(angle))
        tip_y = pos[1] + (7 * speed * scale * math.sin(angle))

        right_x = pos[0] + (3 * speed * scale * math.cos(angle+steepness))
        right_y = pos[1] + (3 * speed * scale * math.sin(angle+steepness))
       
        #pg.draw.circle(surf, SKY_BLUE, (pos[0], pos[1]), 1, 0)
        #pg.draw.circle(surf, WHITE, (start_x, start_y), 1, 0)
        #pg.draw.circle(surf, GREEN, (left_x, left_y), 1, 0)
        #pg.draw.circle(surf, BLUE, (tip_x, tip_y), 1, 0)
        #pg.draw.circle(surf, RED, (right_x, right_y), 1, 0)
        
        spark_points = [(start_x, start_y), (left_x, left_y), (tip_x, tip_y), (right_x, right_y)] 
        #pg.draw.polygon(surf, WHITE, spark_points)

    def click_test_func(self):
        #  p, angle, speed, scale, decay_rate, color, steepness=0.3)
        spark = Spark(
            p=[50,50],
            angle=self.test_angle,
            speed=4,
            scale=0.8, 
            decay_rate=0.92,
            limit=0.3,
            color=WHITE,
            steepness=20
        )
        self.sparks.append(spark)

        spark_collision(self, 10, [80,80], [1,1])


    def check_inputs(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.running = False
                if e.key == pg.K_t:
                    print(f'testing: adding particle')
                    self.click_test_func()
                                        
                if e.key == pg.K_a:
                    self.movement[0] = True 
                if e.key == pg.K_d:
                    self.movement[1] = True
                if e.key == pg.K_w:
                    self.player.jump()
                    self.movement[2] = True 
                if e.key == pg.K_s:
                    self.movement[3] = True
                if e.key == pg.K_q:
                    self.test_angle -= 10
                if e.key == pg.K_e:
                    self.test_angle += 10

            if e.type == pg.KEYUP:
                if e.key == pg.K_a:
                    self.movement[0] = False 
                if e.key == pg.K_d:
                    self.movement[1] = False
                if e.key == pg.K_w:
                    self.movement[2] = False
                if e.key == pg.K_s:
                    self.movement[3] = False

    def run(self):
        while self.running:
            self.check_inputs()
            self.update()
            self.render()

def main():
    gm = GameEngine()
    gm.run()

if __name__ == "__main__":
    main()
