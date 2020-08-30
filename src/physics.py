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

def check_body_wall_collision(body_segments, wall_segments):
    for wall_segment in wall_segments:
        for segment in body_segments:
            PoI = intersect_line_to_line(segment, wall_segment)
            if PoI is not None:
                return True
    return False

def project_ray(start, end, wall_segments):
    segment = (start, end)
    dist = (start-end).length()
    for wall_segment in wall_segments:
        PoI = intersect_line_to_line(segment, wall_segment)
        if PoI is None:
            continue

        delta = (PoI-start).length()
        dist = min(dist, delta)

    return dist

def check_body_gate_collision(body_segments, all_gate_segments):
    for i, gate_segments in enumerate(all_gate_segments):
        for gate_segment in gate_segments: 
            for body_segment in body_segments:
                PoI = intersect_line_to_line(gate_segment, body_segment)
                if PoI:
                    return i
    return None