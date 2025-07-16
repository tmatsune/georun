from settings import *
from utils import * 
from particles import Particle, FloatingParticle

class Player:
    def __init__(self, eng):
        self.eng = eng
        self.radius = PLAYER_RADIUS
        self.color = WHITE
        self.pos = [CENTER[0], CENTER[1]]
        self.size = [PLAYER_NORM_SIZE[0], PLAYER_NORM_SIZE[1]]
        self.vel = [0, 0]
        self.state = 'idle'
        self.jumps = PLAYER_MAX_JUMPS 
        self.speed = PLAYER_SPEED
        self.map_pos = [0,0]
        self.dt_speed = 0
        self.collisions = {'left': False, 'right': False, 'up': False, 'down': False}

    def update_dt_speed(self, dt): return dt * self.speed

    def update_map_pos(self): self.map_pos = [int(self.pos[0]//CS), int(self.pos[1]//CS)]

    def jump(self):
        if self.jumps > 0:
            self.vel[1] = PLAYER_JUMP_SPEED
            self.jumps -= 1

    def update(self, movement, dt):
        self.vel[0] = (movement[1] - movement[0])
        self.vel[1] = min(PLAYER_FALL_SPEED, self.vel[1] + GRAVITY) 
        self.update_map_pos()
        dt_speed = self.update_dt_speed(dt)

        nearby_rects = self.eng.world.get_nearby_rects(self.pos)
        self.movement_handler(dt_speed, self.vel, nearby_rects)

        if self.collisions['up']:
            pass
        if self.collisions['down']:
            self.jumps = PLAYER_MAX_JUMPS
        if self.collisions['left']:
            pass
        if self.collisions['right']:
            pass
        
        self.add_particles()

    def render(self, surf, movement, dt):
        self.update(movement, dt)
        pg.draw.circle(surf, self.color, (self.pos[0]+HALF_CS, self.pos[1]+HALF_CS), self.radius, width=0)
        #pg.draw.rect(surf, WHITE, (self.pos[0], self.pos[1], CS, CS), 1)

    def get_hitable_tiles(self, rect, nearby_tiles):
        hits = []
        for tile in nearby_tiles:
            if rect.colliderect(tile):
                hits.append(tile)
        return hits

    def movement_handler(self, dt_speed, vel, nearby_tiles):
        self.pos[0] += self.vel[0] * dt_speed
        rect = self.rect() 
        hits = self.get_hitable_tiles(self.rect(), nearby_tiles)
        self.collisions = {'left': False, 'right': False, 'up': False, 'down': False}

        for tile in hits:
            if vel[0] > 0:
                rect.right = tile.left
                self.pos[0] = rect.left
                self.collisions['right'] = True
            elif vel[0] < 0:
                rect.left = tile.right
                self.pos[0] = rect.left
                self.collisions['left'] = True

        self.pos[1] += self.vel[1] * dt_speed
        rect = self.rect()
        hits = self.get_hitable_tiles(rect, nearby_tiles)
        for tile in hits:
            if vel[1] > 0:
                rect.bottom = tile.top
                self.pos[1] = rect.y    
                self.collisions['down'] = True
            if vel[1] < 0:
                curr_rect.top = tile.bottom
                self.pos[1] = rect.y
                self.collisions['up'] = True

    def add_particles(self):
        # particle when jumping 
        up, down, left, right = (self.collisions[k] for k in ('up', 'down', 'left', 'right'))
        center = self.center()
        if not up and not down and not left and not right:
            rand_pos = [random.randrange(-3,3) + center[0], center[1] +random.randrange(-3,3)]
            p = Particle(self.eng, rand_pos, v_multiply_scalar(self.vel, -0.8), 3.5, 0.16, WHITE)
            self.eng.particles.append(p)
        else:
            #rand_pos = [random.randrange(-3,3) + center[0], center[1] +random.randrange(-3,3)]
            if rnd_percent_chance(0.45):
                rand_pos = [random.randrange(-2,2) + center[0], center[1] +random.randrange(-3,-1)]
                p = FloatingParticle(
                                    eng=self.eng, 
                                    p=rand_pos, 
                                    v=v_multiply_scalar([random.uniform(-0.3,0.3), -1.4], 0.4), 
                                    r=3, 
                                    decay_rate=random.uniform(0.03,0.06), 
                                    color=WHITE,
                                    amp=random.uniform(-0.2,0.2),  
                                    fq=random.uniform(2, 4)
                                    )
                self.eng.particles.append(p)       

    def rect(self):
        return pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def center(self):
        return [self.pos[0] + self.size[0]//2, self.pos[1] + self.size[1]//2]
        
