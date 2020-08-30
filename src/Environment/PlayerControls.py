import pygame
from .util import clip


class PlayerControls:
    def __init__(self):
        self.accel = 0
        self.brake = 0
        self.wheel = 0

        self.car_keydown = {
            pygame.K_UP: lambda: self.set_accelerator(1),
            pygame.K_DOWN: lambda: self.set_brake(1),
            pygame.K_LEFT: lambda: self.set_wheel(-1),
            pygame.K_RIGHT: lambda: self.set_wheel(1),
        }

        self.car_keyup = {
            pygame.K_UP: lambda: self.set_accelerator(0),
            pygame.K_DOWN: lambda: self.set_brake(0),
            pygame.K_LEFT: lambda: self.set_wheel(1),
            pygame.K_RIGHT: lambda: self.set_wheel(-1),
        }

    def set_accelerator(self, x):
        self.accel = clip(x, 0, 1)
    
    def set_brake(self, x):
        self.brake = clip(x, 0, 1)
    
    def set_wheel(self, x):
        self.wheel = clip(self.wheel+x, -1, 1)
    
    def get_action(self):
        return (self.accel, self.brake, self.wheel)
    
    def on_pygame_event(self, ev):
        if ev.type == pygame.KEYDOWN:
            if ev.key in self.car_keydown:
                self.car_keydown[ev.key]()
                return True
        elif ev.type == pygame.KEYUP:
            if ev.key in self.car_keyup:
                self.car_keyup[ev.key]()
                return True
        
        return False