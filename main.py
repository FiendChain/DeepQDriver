import pygame
from src import Vec2D
from src import Car
from src import Map
from src import Environment, EnvironmentRenderer
from src import Sensor
import pickle

with open("map.pkl", "rb") as fp:
    M = pickle.load(fp)

pygame.init()

screen = pygame.display.set_mode([1500, 900])

running = True

car = Car()
sensor = Sensor(200)

env = Environment(car, sensor, M)
env_render = EnvironmentRenderer()

car_keydown = {
    pygame.K_UP: lambda c: c.set_accelerator(1),
    pygame.K_DOWN: lambda c: c.set_brake(1),
    pygame.K_LEFT: lambda c: c.set_wheel(-1),
    pygame.K_RIGHT: lambda c: c.set_wheel(1),
}

car_keyup = {
    pygame.K_UP: lambda c: c.set_accelerator(0),
    pygame.K_DOWN: lambda c: c.set_brake(0),
    pygame.K_LEFT: lambda c: c.set_wheel(1),
    pygame.K_RIGHT: lambda c: c.set_wheel(-1),
}

while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key in car_keydown:
                car_keydown[ev.key](car)

            if ev.key == pygame.K_r:
                env.reset()

        elif ev.type == pygame.KEYUP:
            if ev.key in car_keyup:
                car_keyup[ev.key](car)
    
    screen.fill((255,255,255))

    env.tick(0.5)
    env_render.render(screen, env)


    pygame.display.flip()

pygame.quit()