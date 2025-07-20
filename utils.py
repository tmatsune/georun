from settings import * 

# render text 
def text_surface(text: str, size: int, italic: bool, rgb: tuple, font='arial', bold=True):
    font = pg.font.SysFont(font, size, bold, italic)
    text_surface = font.render(text, False, rgb)
    return text_surface

# random
def rnd_percent_chance(probability_per_frame=0.1):
    return random.random() < probability_per_frame

# other 
def swap_color(img, old_c, new_c):
    global e_colorkey
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img, (0, 0))
    return surf

def silhouette(surf, color=(255, 255, 255)):
    mask = pg.mask.from_surface(surf)
    new_surf = swap_color(mask.to_surface(), (255, 255, 255), color)
    new_surf.set_colorkey((0, 0, 0))
    return new_surf

def outline(target, src, pos, color):
    s = silhouette(src, color=color)
    for shift in [[0, 1], [1, 0], [-1, 0], [0, -1]]:
        target.blit(s, (pos[0] + shift[0], pos[1] + shift[1]))

# easing functions
def linear_scale(value, in_min, in_max, out_min, out_max):
    # Clamp input to avoid overshooting
    value = max(min(value, in_max), in_min)
    return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)

def nonlinear_scale(value, in_min, in_max, out_min, out_max, power=0.7):
    value = max(min(abs(value), in_max), in_min)        # 1. Clamp input
    norm = (value - in_min) / (in_max - in_min)         # 2. Normalize
    curved = norm ** power                              # 3. Nonlinear curve
    return out_min + curved * (out_max - out_min)       # 4. Map to scale range

# math 
def distance(a, b):
    return math.sqrt(math.pow(abs(a[0] - b[0]), 2) + math.pow(a[1] - b[1], 2))

# vector functions
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def normalize(v):
    res = v.copy()
    l = v_length(v)
    res[0] = res[0] / l
    res[1] = res[1] / l
    return res

def v_length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])

def v_add(a, b):
    return [a[0]+b[0], a[1]+b[1]]

def v_multiply_scalar(v, x):
    return [v[0] * x, v[1] * x]

def v_angle(v):
    angle_rad = math.atan2(v[1], v[0])
    angle_deg = math.degrees(angle_rad)
    return angle_deg


