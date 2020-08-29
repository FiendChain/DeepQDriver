import pygame
from src import Car, Map, Environment, Sensor, EnvironmentRenderer
import pickle
import time
import numpy as np

with open("map.pkl", "rb") as fp:
    M = pickle.load(fp)

car = Car()
sensor = Sensor(200)
env = Environment(car, sensor, M)

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
model.load_weights("dqn_weights.h5f")
print(model.summary())


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

    _, reward, _, _ = env.step(action, reset_finished=False)
    env_render.render(screen, env)

    if reward != 0:
        print(f"reward: {reward}")

    pygame.display.flip()

pygame.quit()