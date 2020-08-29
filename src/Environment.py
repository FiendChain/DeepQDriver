import math
from .Vec2D import Vec2D

from .util import get_points
from .physics import intersect_line_to_line

from .Sensor import Sensor

class Environment:
    def __init__(self, car, sensor, M):
        self.car = car
        self.map = M
        self.sensor = sensor

        self.reset()

        wall_segments = []
        wall_segments.extend(list(zip(M.outer[:-1], M.outer[1:])))
        wall_segments.append((M.outer[0], M.outer[-1]))
        wall_segments.extend(list(zip(M.inner[:-1], M.inner[1:])))
        wall_segments.append((M.inner[0], M.inner[-1]))

        wall_segments = [(Vec2D.from_tuple(p1), Vec2D.from_tuple(p2)) for p1, p2 in wall_segments]
        self.wall_segments = wall_segments
    
    def tick(self, dt):
        self.car.tick(dt)
        self.sensor.update(self.car.pos, self.car.dir, self.wall_segments)

        if self.check_collision():
            self.reset()


    def check_collision(self):
        car = self.car
        M = self.map

        body_points = get_points(car.pos, car.dir, car.dim)
        body_segments = list(zip(body_points[1:], body_points[:-1]))
        
        for body_segment in body_segments:
            for wall_segment in self.wall_segments:
                PoI = intersect_line_to_line(body_segment, wall_segment)
                if PoI is not None:
                    return True
        
        return False


    def reset(self):
        car = self.car

        pos = Vec2D.from_tuple(self.map.path[0])
        nxt = Vec2D.from_tuple(self.map.path[1])
        diff_vec = nxt-pos
        dir_angle = math.atan(diff_vec.x/diff_vec.y)

        car.pos = pos
        car.dir = math.pi+dir_angle
        car.vel = Vec2D(0,0)

        self.sensor.reset()