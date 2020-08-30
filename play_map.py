import pygame
from src.Environment import *
import pickle

from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("map_file")
    args = parser.parse_args()

    with open(args.map_file, "rb") as fp:
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
        observation, reward, done, info = env.step(action, reset_finished=False)
        env_render.render(screen, env)

        if reward != 0:
            print(f"reward: {reward}")


        pygame.display.flip()

    pygame.quit()

    env.on_exit()

if __name__ == '__main__':
    main()