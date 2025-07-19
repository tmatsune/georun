from settings import * 

# random
def rnd_percent_chance(probability_per_frame=0.1):
    return random.random() < probability_per_frame

# other 
def deg_to_rad(deg): return deg * (math.pi/180)


def linear_scale(value, in_min, in_max, out_min, out_max):
    # Clamp input to avoid overshooting
    value = max(min(value, in_max), in_min)
    return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)

def nonlinear_scale(value, in_min, in_max, out_min, out_max, power=0.7):
    value = max(min(abs(value), in_max), in_min)        # 1. Clamp input
    norm = (value - in_min) / (in_max - in_min)         # 2. Normalize
    curved = norm ** power                              # 3. Nonlinear curve
    return out_min + curved * (out_max - out_min)       # 4. Map to scale range

# Vector Functions
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


