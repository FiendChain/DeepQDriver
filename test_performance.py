from src import Vec2D
from src import Car
from src import Map
from src import Environment
from src import Sensor
import pickle

import time

with open("map.pkl", "rb") as fp:
    M = pickle.load(fp)


car = Car()
sensor = Sensor(200)

env = Environment(car, sensor, M)

last_frame = time.perf_counter()

try:
    while True:
        env.tick(1)
        curr_frame = time.perf_counter()
        dt = curr_frame-last_frame
        fps = 1/dt
        print(f"fps: {int(fps):5d}\r", end='')
        last_frame = curr_frame
except KeyboardInterrupt:
    pass
