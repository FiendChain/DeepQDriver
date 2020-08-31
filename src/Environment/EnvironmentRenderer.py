import pygame

from .MapRenderer import MapRenderer
from .CarRenderer import CarRenderer
from .SensorRenderer import SensorRenderer

class EnvironmentRenderer:
    def __init__(self):
        self.map_rend = MapRenderer()
        self.car_rend = CarRenderer()
        self.sensor_rend = SensorRenderer()

        self.show_map = True
        self.show_car = True
        self.show_sensor = True

    def render(self, surface, env):
        if self.show_map:
            self.map_rend.render(surface, env.map)

        # if env.collided:
        #     self.car_rend.body_colour = (255,0,0)
        # else:
        #     self.car_rend.body_colour = (0,0,255)

        if self.show_car:
            self.car_rend.render(surface, env.car)

        if self.show_sensor:
            self.sensor_rend.render(surface, env.car.pos, env.car.dir, env.sensor)