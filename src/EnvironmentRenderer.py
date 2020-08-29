import pygame

from .MapRenderer import MapRenderer
from .CarRenderer import CarRenderer
from .SensorRenderer import SensorRenderer

class EnvironmentRenderer:
    def __init__(self):
        self.map_rend = MapRenderer()
        self.car_rend = CarRenderer()
        self.sensor_rend = SensorRenderer()

    def render(self, surface, env):
        self.map_rend.render(surface, env.map)

        # if env.collided:
        #     self.car_rend.body_colour = (255,0,0)
        # else:
        #     self.car_rend.body_colour = (0,0,255)

        self.car_rend.render(surface, env.car)

        self.sensor_rend.render(surface, env.car.pos, env.car.dir, env.sensor)