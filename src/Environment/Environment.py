import math
from .Vec2D import Vec2D
from .BakedMap import BakedMap
from .ThreadedBakedMap import ThreadedBakedMap

from .util import get_points
from .physics import intersect_line_to_line

from .Sensor import Sensor


class Environment:
    def __init__(self, car, sensor, M):
        self.car = car
        self.map = M
        self.baked_map = BakedMap(M) 
        # self.baked_map = ThreadedBakedMap(M) 
        self.baked_map.summary()

        self.sensor = sensor
        self.reset()

    
    def step(self, action, dt=1, reset_finished=True):
        self.car.set_action(action)
        self.car.tick(dt)
        self.sensor.update(self.car, self.baked_map)

        segments = self.car.get_segments()

        self.last_gate_ticks += 1 

        info = {'gate': self.last_gate}

        if self.baked_map.check_wall_collision(segments):
            self.reset()
            return self.get_observation(), -100, True, info

        
        idx = self.baked_map.check_gate_collision(segments)
        if idx is None:
            return self.get_observation(), 0, False, info

        # passed checkpoint
        if idx != 0 and idx > self.last_gate:
            reward = 10000 / (self.last_gate_ticks**1.5)
            done = False
            self.last_gate_ticks = 0 
        # completed a full loop
        elif idx == 0 and self.last_gate == self.baked_map.total_gates-1:
            reward = 10000 / (self.last_gate_ticks**1.5)
            done = reset_finished
            self.last_gate_ticks = 0 
        # ended up backwards
        elif idx != self.last_gate:
            reward = -100
            done = True
            self.last_gate_ticks = 0 
        # if too many ticks, then car just doing nothing
        elif idx == self.last_gate and self.last_gate_ticks > 1000:
            done = True
            reward = 0
        # just at the same gate
        else:
            done = False
            reward = 0

        self.last_gate = idx

        rv = self.get_observation(), reward, done, info 
        if done:
            self.reset()
        return rv
    
    def get_observation(self):
        return self.sensor.data

    def reset(self):
        car = self.car

        pos0, dir0 = self.baked_map.get_spawn()

        car.pos = pos0
        car.dir = dir0
        car.vel = Vec2D(0,0)

        self.last_gate = 0
        self.last_gate_ticks = 0

        self.sensor.reset()

        return self.get_observation()
    
    def on_exit(self):
        self.baked_map.on_exit()