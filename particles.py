from settings import * 
from utils import *

class Particle:
    def __init__(self, eng, p, v, r, decay_rate, color):
        self.eng = eng
        self.pos = p.copy()
        self.vel = v.copy() 
        self.rad = r
        self.decay_rate = decay_rate
        self.color = color 
        self.done = False

    def update(self, dt):
        self.rad -= self.decay_rate
        if self.rad < 0.1:
            self.done = True
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
            
    def render(self, surf, dt):
        self.update(dt)
        pg.draw.circle(surf, self.color, (self.pos[0], self.pos[1]), self.rad, width=0)

class FloatingParticle(Particle):
    def __init__(self, eng, p, v, r, decay_rate, color, amp, fq):
        super().__init__(eng, p, v, r, decay_rate, color)
        self.amp = amp 
        self.fq = fq

    def update(self, dt):
        super().update(dt)
        self.vel[0] = self.amp * math.sin(self.eng.tt * self.fq)

    def render(self, surf, dt):
        super().render(surf, dt)

class Spark:
    def __init__(self, p, angle, speed, scale, decay_rate, limit, color, steepness=0.3):
        self.pos = p.copy()
        self.angle = math.radians(angle)
        self.speed = speed
        self.scale = scale
        self.decay_rate = decay_rate
        self.limit = limit
        self.color = color
        self.steepness = math.radians(steepness)
        self.vel = self.get_vel_v(self.angle)
        self.done = False

    def get_vel_v(self, a):
        v = [math.cos(self.angle), math.sin(self.angle)]
        return normalize(v)
    
    def update(self, dt):
        self.pos[0] += self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.speed
        self.speed *= self.decay_rate
        if self.speed < self.limit:
            self.done = True

    def render(self, surf, dt):
        self.update(dt)
        pos = self.pos
        speed = self.speed 
        scale = self.scale
        angle = self.angle 
        steepness = self.steepness
        start_x = pos[0] + (.1 * speed * scale * math.cos(angle))
        start_y = pos[1] + (.1 * speed * scale * math.sin(angle))
        left_x = pos[0] +  (3 * speed * scale * math.cos(angle-steepness))
        left_y = pos[1] +  (3 * speed * scale * math.sin(angle-steepness))
        tip_x = pos[0] + (7 * speed * scale * math.cos(angle))
        tip_y = pos[1] + (7 * speed * scale * math.sin(angle))
        right_x = pos[0] + (3 * speed * scale * math.cos(angle+steepness))
        right_y = pos[1] + (3 * speed * scale * math.sin(angle+steepness))
        points = [
            [start_x, start_y],
            [left_x, left_y],
            [tip_x, tip_y],
            [right_x, right_y]
        ]
        pg.draw.polygon(surf, self.color, points)

def spark_collision(eng, amnt, pos, vel, color, rnd_range=30):
    vel = v_multiply_scalar(vel, -1)
    angle = v_angle(vel)
    offset = [math.cos(math.atan(angle))*16, math.sin(math.atan(angle))*16]
    for i in range(amnt): 
        rnd_angle = angle + random.randrange(-rnd_range,rnd_range)
        speed = random.uniform(3.5, 4.5)
        d_rate = random.uniform(0.9, 0.95)
        spark = Spark(
                p=[pos[0]-offset[0], pos[1]-offset[1]],
                angle=rnd_angle,
                speed=speed,
                scale=0.8, 
                decay_rate=d_rate,
                limit=0.3,
                color=color,
                steepness=20
            )
        eng.sparks.append(spark)
