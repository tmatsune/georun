from settings import *
from utils import * 
from particles import Particle, FloatingParticle, spark_collision

class Player:
    def __init__(self, eng):
        self.eng = eng
        self.radius = PLAYER_RADIUS
        self.color = RED_P
        self.pos = [CENTER[0], CENTER[1]]
        self.size = [PLAYER_NORM_SIZE[0], PLAYER_NORM_SIZE[1]]
        self.vel = [0, 0]
        self.state = 'idle'
        self.jumps = PLAYER_MAX_JUMPS 
        self.speed = PLAYER_SPEED
        self.map_pos = [0,0]
        self.dt_speed = 0
        self.collisions = {'left': False, 'right': False, 'up': False, 'down': False}
        self.first_hit = {'left': False, 'right': False, 'up': False, 'down': False}
        self.was_colliding = {'left': False, 'right': False, 'up': False, 'down': False}
        self.kick_back = [0,0]
        self.bounce = False

    def update_dt_speed(self, dt): 
        return dt * self.speed

    def update_map_pos(self): 
        self.map_pos = [int(self.pos[0]//CS), int(self.pos[1]//CS)]

    def jump(self):
        if self.jumps > 0:
            self.vel[1] = PLAYER_JUMP_SPEED
            self.jumps -= 1

    def bounce_handler(self):
        if self.first_hit['down']:
            self.bounce = True
        if self.bounce: 
            self.vel[1] *= -0.6
        if abs(self.vel[1]) < 0.2:
            self.bounce = False
            self.vel[1] = PLAYER_FALL_SPEED

    def update(self, movement, dt):
        acc = (movement[1] - movement[0]) * 0.4
        if acc:
            self.vel[0] += acc #+ self.kick_back[0]
        else:
            if self.collisions['down']:
                friction = 0.05
            else:
                friction = 0.01
                
            if self.vel[0] > 0:
                self.vel[0] = max(self.vel[0] - friction, 0)
            elif self.vel[0] < 0:
                self.vel[0] = min(self.vel[0] + friction, 0)
        max_speed = 1
        self.vel[0] += self.kick_back[0]
        self.vel[0] = max(min(self.vel[0], max_speed), -max_speed)

        self.vel[1] = min(PLAYER_FALL_SPEED, self.vel[1] + GRAVITY) 
        self.update_map_pos()
        dt_speed = self.update_dt_speed(dt)

        if abs(self.kick_back[0]) > 0.2: self.kick_back[0] *= 0.9
        else: self.kick_back[0] = 0

        nearby_rects = self.eng.world.get_nearby_rects(self.pos)
        self.movement_handler(dt_speed, self.vel, nearby_rects)

        if self.collisions['up']:
            if not self.was_colliding['up']: self.first_hit['up'] = True  
            else: self.first_hit['up'] = False 
            self.was_colliding['up'] = True
        else:
            self.first_hit['up'] = False
            self.was_colliding['up'] = False

        if self.collisions['down']:
            self.jumps = PLAYER_MAX_JUMPS
            if not self.was_colliding['down']:
                self.first_hit['down'] = True  
            else:
                self.first_hit['down'] = False 
            self.was_colliding['down'] = True
            self.bounce_handler()
        else:
            self.first_hit['down'] = False
            self.was_colliding['down'] = False

        if self.collisions['left']:
            if not self.was_colliding['left']: self.first_hit['left'] = True  
            else: self.first_hit['left'] = False 
            self.was_colliding['left'] = True
        else:
            self.first_hit['left'] = False
            self.was_colliding['left'] = False

        if self.collisions['right']:
            if not self.was_colliding['right']: self.first_hit['right'] = True  
            else: self.first_hit['right'] = False 
            self.was_colliding['right'] = True
        else:
            self.first_hit['right'] = False
            self.was_colliding['right'] = False
        
        self.add_particles()

    def render(self, surf, movement, dt):
        self.update(movement, dt)
        pg.draw.circle(surf, self.color, (self.pos[0]+HALF_CS, self.pos[1]+HALF_CS), self.radius, width=0)
        pos = self.center()
        pg.draw.circle(surf, WHITE, (pos[0], pos[1]), 5, width=0)

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
                rect.top = tile.bottom
                self.pos[1] = rect.y
                self.collisions['up'] = True

    def add_particles(self):
        # particle when jumping
        up, down, left, right = (self.collisions[k] for k in ('up', 'down', 'left', 'right'))
        fup, fdown, fleft, fright = (self.first_hit[k] for k in ('up', 'down', 'left', 'right'))
        center = self.center()
        if not up and not down and not left and not right:
            rand_pos = [random.randrange(-3,3) + center[0], center[1] +random.randrange(-3,3)]
            p = Particle(self.eng, rand_pos, v_multiply_scalar(self.vel, -0.8), 3.5, 0.16, WHITE)
            self.eng.particles.append(p)
        elif (left and fleft) or (right and fright) or (down and fdown):
            s_vel = [0,0]
            if left: 
                self.vel[0] = 1
                s_vel = [1, 0]
                spark_collision(eng=self.eng, amnt=14, pos=self.center(), vel=s_vel, color=RED_P, scale=0.6,rnd_range=50)
            elif right: 
                self.kick_back[0] = -2.5
                s_vel = [1, 0]
                spark_collision(eng=self.eng, amnt=14, pos=self.center(), vel=s_vel, color=RED_P, scale=0.6,rnd_range=50)
            elif down:
                s_vel = [0, 1]
                scale = 0
                decay_rate = [0.9, 0.95]
                if self.vel[1] == 2: 
                    scale = 0.1
                    decay_rate = [0.65, 0.75]
                else:  # scale = abs(self.vel[1]) * 0.6
                    decay = linear_scale(value=abs(self.vel[1]), in_min=0.1, in_max=2.0, out_min=0.9, out_max=0.95)
                    decay_rate = [decay - 0.1, decay]
                    scale = nonlinear_scale(value=abs(self.vel[1]), in_min=0.1, in_max=2.0, out_min=0.2, out_max=0.8)

                spark_collision(
                    eng=self.eng, 
                    amnt=14, 
                    pos=self.center(), 
                    vel=s_vel, 
                    color=RED_P, 
                    scale=scale,
                    rnd_range=60,
                    decay_rate=decay_rate
                    )
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

    def rect(self): return pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    def center(self): return [self.pos[0] + self.size[0]//2, self.pos[1] + self.size[1]//2]
