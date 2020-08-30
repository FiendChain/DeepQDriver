import math
from .Vec2D import Vec2D

def point_rot(p, sin, cos=None):
    if cos is None:
        sin, cos = math.sin(sin), math.cos(sin)

    x = cos*p.x - sin*p.y
    y = sin*p.x + cos*p.y
    return Vec2D(x, y)

def clip(x, _min=0, _max=1):
    return min(max(x, _min), _max)

def get_points(pos, dir_angle, dim):
    off = dim/2

    sin, cos = math.sin(dir_angle), math.cos(dir_angle)

    p1 = pos + point_rot(Vec2D(+off.x, +off.y), sin, cos)
    p2 = pos + point_rot(Vec2D(-off.x, +off.y), sin, cos)
    p3 = pos + point_rot(Vec2D(+off.x, -off.y), sin, cos)
    p4 = pos + point_rot(Vec2D(-off.x, -off.y), sin, cos)

    return (p1, p2, p4, p3)