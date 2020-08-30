import pygame
from .Vec2D import Vec2D
from .util import point_rot

class SensorRenderer:
    def __init__(self):
        self.ray_colour = (0,255,0)
        self.intersect_colour = (0,127,0)
    
    def render(self, surface, pos, dir_angle, sensor):
        rays = [pos+point_rot(ray, dir_angle)*val for val, ray in zip(sensor.data, sensor.rays)]

        pos_tup = pos.cast_tuple(int)

        for ray in rays:
            pygame.draw.line(surface, self.ray_colour, pos_tup, ray.cast_tuple(int))
        
        for ray in rays:
            pygame.draw.circle(surface, self.intersect_colour, ray.cast_tuple(int), 5)


