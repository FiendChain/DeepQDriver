import pygame
from src.Environment import *
import pickle
import time
import numpy as np
from argparse import ArgumentParser

from src.Agents import EnvironmentWrapper, dqn_controls, create_dqn_model

def main():
    parser = ArgumentParser()
    parser.add_argument("map_file")
    parser.add_argument("ai_file")
    parser.add_argument("--drift", action="store_true")

    args = parser.parse_args()

    with open(args.map_file, "rb") as fp:
        M = pickle.load(fp)

    car = Car()
    car.drift = args.drift
    car.C_drift_control = 0.3
    car.C_drift_traction = 0.4
    car.C_drift_sideslip = 0.3
    car.F_engine_max = 10

    # sensor = Sensor(300, total=16)
    sensor = NonLinearSensor(300, total=16)

    env = Environment(car, sensor, M)
    env = EnvironmentWrapper(dqn_controls, env)

    from keras.models import Sequential
    from keras.layers import Dense, Activation, Flatten

    model = create_dqn_model(env)
    print(model.summary())

    # model.load_weights("dqn_weights.h5f")
    # model.load_weights("dqn_drift_weights.h5f")
    model.load_weights(args.ai_file)

    pygame.init()
    screen = pygame.display.set_mode([1500, 900])

    env_render = EnvironmentRenderer()

    running = True

    curr_tick = 0
    action = None

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    curr_tick = 0
                    env.reset()
                elif ev.key == pygame.K_s:
                    env_render.show_sensor = not env_render.show_sensor
                elif ev.key == pygame.K_d:
                    car.drift = not car.drift
                    print(f"drift={car.drift}")

        
        screen.fill((255,255,255))

        if curr_tick % 1 == 0 or action is None:
            observation = env.get_observation()
            observation = np.array(observation).reshape((1,1,env.nb_observations))

            action = model.predict(observation)
            action = np.argmax(action[0])

        _, reward, _, _ = env.step(action, reset_finished=False, dt=1)
        curr_tick += 1
        env_render.render(screen, env)


        if reward != 0:
            print(f"reward: {reward}")

        pygame.display.flip()

    pygame.quit()

    env.on_exit()

if __name__ == '__main__':
    main()