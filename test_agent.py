import pygame
from src.Environment import *
import pickle
import time
import numpy as np
from argparse import ArgumentParser

from src.Agents import EnvironmentWrapper, dqn_controls

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

    sensor = Sensor(200)

    env = Environment(car, sensor, M)
    env = EnvironmentWrapper(dqn_controls, env)

    from keras.models import Sequential
    from keras.layers import Dense, Activation, Flatten

    nb_actions = 3

    model = Sequential()
    model.add(Flatten(input_shape=(1,8)))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))
    print(model.summary())

    # model.load_weights("dqn_weights.h5f")
    # model.load_weights("dqn_drift_weights.h5f")
    model.load_weights(args.ai_file)

    pygame.init()
    screen = pygame.display.set_mode([1500, 900])

    env_render = EnvironmentRenderer()

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    env.reset()
        
        screen.fill((255,255,255))

        observation = env.get_observation()
        observation = np.array(observation).reshape((1,1,8))

        action = model.predict(observation)
        action = np.argmax(action[0])

        _, reward, _, _ = env.step(action, reset_finished=False, dt=1)
        env_render.render(screen, env)

        if reward != 0:
            print(f"reward: {reward}")

        pygame.display.flip()

    pygame.quit()

    env.on_exit()

if __name__ == '__main__':
    main()