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

        self.angles =  np.linspace(0, math.pi*2, total+1)[:-1]
        self.rays = [point_rot(Vec2D(0,dist), alpha) for alpha in self.angles]
    
    def reset(self):
        for i in range(len(self.data)):
            self.data[i] = 1
    
    def update(self, pos, dir_angle, segments):
        self.reset()

        ray_segments = [(pos, pos+point_rot(ray, dir_angle)) for ray in self.rays] 

        for i, ray_seg in enumerate(ray_segments):
            for wall_seg in segments:
                PoI = intersect_line_to_line(ray_seg, wall_seg)
                if PoI is None:
                    continue

                delta = (PoI-pos).length()
                self.data[i] = min(delta/self.dist, self.data[i])
        


    