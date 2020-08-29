import pygame
from src import Vec2D
from src import Car
from src import Map
from src import Environment, EnvironmentRenderer
from src import Sensor
from src import PlayerControls
import pickle

with open("map.pkl", "rb") as fp:
    M = pickle.load(fp)

pygame.init()

screen = pygame.display.set_mode([1500, 900])

running = True

car = Car()
player_controls = PlayerControls()
sensor = Sensor(200)

env = Environment(car, sensor, M)
env_render = EnvironmentRenderer()

while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif player_controls.on_pygame_event(ev):
            continue
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_r:
                env.reset()
    
    screen.fill((255,255,255))

    action = player_controls.get_action()
    reward = env.tick(action, 1)
    env_render.render(screen, env)

    if reward != 0:
        print(f"reward: {reward}")


    pygame.display.flip()

pygame.quit()