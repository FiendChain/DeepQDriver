import math
from .Vec2D import Vec2D

class Environment:
    def __init__(self, car, M):
        self.car = car
        self.map = M

        self.reset()
    
    def tick(self, dt):
        self.car.tick(dt)

    def reset(self):
        car = self.car

        pos = Vec2D.from_tuple(self.map.path[0])
        nxt = Vec2D.from_tuple(self.map.path[1])
        diff_vec = nxt-pos
        dir_angle = math.atan(diff_vec.x/diff_vec.y)

        car.pos = pos
        car.dir = math.pi+dir_angle
        car.vel = Vec2D(0,0)