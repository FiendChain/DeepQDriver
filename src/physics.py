import math
from .Vec2D import Vec2D

def intersect_line_to_line(L1, L2):
    u0, t0 = L1
    u1, t1 = L2

    v0 = t0-u0
    v1 = t1-u1

    x00, y00 = u0.x, u0.y
    x10, y10 = u1.x, u1.y
    x01, y01 = v0.x, v0.y
    x11, y11 = v1.x, v1.y

    d = x11*y01 - x01*y11

    if d == 0:
        return None
    
    s = (1/d) * +(+(x00-x10)*y01 - (y00-y10)*x01)
    t = (1/d) * -(-(x00-x10)*y11 + (y00-y10)*x11)

    if 0 < s < 1 and 0 < t < 1:
        return u0 + t*v0
    
    return None