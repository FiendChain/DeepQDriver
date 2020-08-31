import math
import numpy as np
from .Vec2D import Vec2D
from .util import point_rot
from .physics import intersect_line_to_line

class Sensor:
    def __init__(self, dist, total=8):
        self.dist = dist
        self.total = total
        self.data = [1 for _ in range(total)]
        
        self.rays = self.generate_rays(total, dist)

    def generate_rays(self, total, dist):
        angles =  np.linspace(0, math.pi*2, total+1)[:-1]
        rays = [point_rot(Vec2D(0, dist), alpha) for alpha in angles]
        return rays
    
    def reset(self):
        for i in range(len(self.data)):
            self.data[i] = 1
    
    def update(self, car, baked_map):
        self.reset()

        start = car.pos
        for i, ray in enumerate(self.rays):
            end = car.pos+point_rot(ray, car.dir)
            dist = baked_map.project_ray(start, end)
            if dist is not None:
                self.data[i] = min(dist/self.dist, self.data[i])

class NonLinearSensor(Sensor):
    def __init__(self, dist, total=8, density=0.3):
        self.density = density
        super().__init__(dist, total=total)

    def generate_rays(self, total, dist):
        steps = np.linspace(0, 1, total+1)[:-1]
        angle_delta = np.array([(math.sin(x*math.pi*4)+1)/2+self.density for x in steps])
        delta_norm = angle_delta/sum(angle_delta)

        angles = []
        curr_angle = 0
        for delta in delta_norm:
            angles.append(curr_angle)
            curr_angle += delta*math.pi*2

        rays = [point_rot(Vec2D(0, dist), alpha) for alpha in angles]
        return rays
        

        


    