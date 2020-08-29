import pygame

from .MapRenderer import MapRenderer
from .CarRenderer import CarRenderer

class EnvironmentRenderer:
    def __init__(self):
        self.map_rend = MapRenderer()
        self.car_rend = CarRenderer()

    def render(self, surface, env):
        self.map_rend.render(surface, env.map)
        self.car_rend.render(surface, env.car)