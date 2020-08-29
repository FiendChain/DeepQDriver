import math
from .Vec2D import Vec2D

from .util import get_points
from .physics import intersect_line_to_line

from .Sensor import Sensor

class Environment:
    def __init__(self, car, sensor, M):
        self.car = car
        self.map = M
        self.sensor = sensor

        self.reset()

        wall_segments = []
        wall_segments.extend(list(zip(M.outer[:-1], M.outer[1:])))
        wall_segments.append((M.outer[0], M.outer[-1]))
        wall_segments.extend(list(zip(M.inner[:-1], M.inner[1:])))
        wall_segments.append((M.inner[0], M.inner[-1]))

        wall_segments = [(Vec2D.from_tuple(p1), Vec2D.from_tuple(p2)) for p1, p2 in wall_segments]
        self.wall_segments = wall_segments

        all_gate_segments = []
        for gate in self.map.gates:
            gate_segments = []
            gate_segments.extend(list(zip(gate[:-1], gate[1:])))
            gate_segments.append((gate[0], gate[-1]))

            gate_segments = [(Vec2D.from_tuple(p1), Vec2D.from_tuple(p2)) for p1, p2 in gate_segments]

            all_gate_segments.append(gate_segments)
        
        self.all_gate_segments = all_gate_segments
    
    def step(self, action, dt=1, reset_finished=True):
        self.car.set_action(action)
        self.car.tick(dt)
        self.sensor.update(self.car.pos, self.car.dir, self.wall_segments)

        self.last_gate_ticks += 1 

        if self.check_collision():
            self.reset()
            return self.get_observation(), -100, True, {}

        
        idx = self.check_gate()
        if idx is None:
            return self.get_observation(), 0, False, {}

        # passed checkpoint
        if idx != 0 and idx > self.last_gate:
            reward = 10000 / (self.last_gate_ticks**1.5)
            done = False
            self.last_gate_ticks = 0 
        # completed a full loop
        elif idx == 0 and self.last_gate == len(self.map.gates)-1:
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

        rv = self.get_observation(), reward, done, {}
        if done:
            self.reset()
        return rv
    
    def get_observation(self):
        return self.sensor.data

    def check_collision(self):
        car = self.car
        M = self.map

        body_points = get_points(car.pos, car.dir, car.dim)
        body_segments = list(zip(body_points[1:], body_points[:-1]))
        
        for body_segment in body_segments:
            for wall_segment in self.wall_segments:
                PoI = intersect_line_to_line(body_segment, wall_segment)
                if PoI is not None:
                    return True
        
        return False

    def check_gate(self):
        car = self.car
        gates = self.map.gates

        body_points = get_points(car.pos, car.dir, car.dim)
        body_segments = list(zip(body_points[1:], body_points[:-1]))

        for i, gate_segments in enumerate(self.all_gate_segments):
            for gate_segment in gate_segments: 
                for body_segment in body_segments:
                    PoI = intersect_line_to_line(gate_segment, body_segment)
                    if PoI:
                        return i

        return None


    def reset(self):
        car = self.car

        pos = Vec2D.from_tuple(self.map.path[0])
        nxt = Vec2D.from_tuple(self.map.path[1])
        diff_vec = nxt-pos
        dir_angle = math.atan(diff_vec.x/diff_vec.y)

        car.pos = pos
        car.dir = math.pi+dir_angle
        car.vel = Vec2D(0,0)


        self.last_gate = 0
        self.last_gate_ticks = 0

        self.sensor.reset()

        return self.get_observation()