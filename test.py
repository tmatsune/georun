import math 

def deg_to_rad(deg): return deg * (math.pi/180)
def v_length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])

v = [1,1]
def norm(v):
    res = v.copy()
    l = v_length(v)
    res[0] = res[0] / l
    res[1] = res[1] / l
    return res

def map_value(value, in_min, in_max, out_min, out_max):
    # Clamp input to avoid overshooting
    value = max(min(value, in_max), in_min)
    return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)

vel = -1.25  # example velocity, should be negative
scale = map_value(abs(vel), 0.0, 2.0, 0.1, 0.8)
print(scale)

''' 
pg.draw.rect(self.eng.surf, GREEN, curr_rect)
                    TOP_LEFT  TOP_RIGHT BTM_RIGHT BTM_LEFT
rectangle_points = [(50, 50), (60, 50), (60, 60), (50, 60)]
pg.draw.polygon(surf, WHITE, rectangle_points)

tgt_x = pos[0] + (pos[0] * self.test_l * math.cos(angle))
tgt_y = pos[1] + (pos[1] * self.test_l * math.sin(angle))



        right_x = pos[0] + (pos[0] * .05 * math.cos(angle-steepness))
        right_y = pos[1] + (pos[1] * .05 * math.sin(angle-steepness))
        right_pos = [right_x, right_y]
        
        pg.draw.circle(surf, WHITE, (pos[0], pos[1]), 1, 0)
        pg.draw.circle(surf, GREEN, (tgt_pos[0], tgt_pos[1]), 1, 0)
        pg.draw.circle(surf, BLUE, (left_pos[0], left_pos[1]), 1, 0)
        pg.draw.circle(surf, RED, (right_pos[0], right_pos[1]), 1, 0)
        
        spark_points = [(pos[0], pos[1]), (left_x, left_y), (tgt_x, tgt_y), (right_x, right_y)] 
        pg.draw.polygon(surf, WHITE, spark_points)
        if rnd_percent_chance(0.95):
            self.test_l -= 0.006
            if self.test_l < 0.01:
                self.test_pos = [600,600]

----------------------------

    def test_func(self, surf):
        pos = self.test_pos.copy()
        angle = deg_to_rad(self.test_angle)
        speed = 2
        scale = 2
        points = [
            [pos[0] + math.cos(angle) * speed * scale, pos[1] + math.sin(angle) * speed * scale],
            [pos[0] + math.cos(angle + math.pi / 2) * speed * scale * 0.3, pos[1] + math.sin(angle + math.pi / 2) * speed * scale * 0.3],
            [pos[0] - math.cos(angle) * speed * scale * 4, pos[1] - math.sin(angle) * speed * scale * 4],
            [pos[0] + math.cos(angle - math.pi / 2) * speed * scale * 0.3, pos[1] - math.sin(angle + math.pi / 2) * speed * scale * 0.3]
        ]
        pg.draw.polygon(surf, WHITE, points)    

----------------------------
'''

