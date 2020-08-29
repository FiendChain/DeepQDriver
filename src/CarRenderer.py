import pygame

from .Vec2D import Vec2D
from .util import get_points, point_rot

class CarRenderer:
    def __init__(self):
        self.body_color = (0,0,255)
        self.wheel_colour = (30,30,30)
    
    def render(self, surface, car):
        body = self.get_body_poly(car)
        wheels = self.get_wheel_polys(car)

        pygame.draw.polygon(surface, self.body_color, self.cast_poly(body))
        for wheel in wheels:
            pygame.draw.polygon(surface, self.wheel_colour, self.cast_poly(wheel))
        
        self.render_motion_vec(surface, car)
    
    def cast_poly(self, poly):
        return list(map(lambda p: p.cast_tuple(int), poly))
    
    def render_motion_vec(self, surface, car):
        start_pt = car.pos.cast_tuple(int)

        dir_vec = point_rot(Vec2D(0,1), car.dir)
        dir_pt = (car.pos+dir_vec*20).cast_tuple(int)
        vel_pt = (car.pos+car.vel.norm()*20).cast_tuple(int)

        pygame.draw.line(surface, (255,0,0), start_pt, dir_pt)
        pygame.draw.line(surface, (0,255,0), start_pt, vel_pt)

    def get_body_poly(self, car):
        return get_points(car.pos, car.dir, car.dim)
    
    def get_wheel_polys(self, car):
        wheel_x = (car.dim.x/2) * 0.9
        wheel_y = (car.dim.y/2) * 0.9
        wheel_dim = car.dim/3

        wheel_angle = car.wheel*car.wheel_angle_max

        def get_wheel_pos(x, y):
            off = point_rot(Vec2D(x,y), car.dir)
            return car.pos+off


        return [
            get_points(get_wheel_pos(-wheel_x, +wheel_y), car.dir+wheel_angle, wheel_dim),
            get_points(get_wheel_pos(+wheel_x, +wheel_y), car.dir+wheel_angle, wheel_dim),
            get_points(get_wheel_pos(-wheel_x, -wheel_y), car.dir, wheel_dim),
            get_points(get_wheel_pos(+wheel_x, -wheel_y), car.dir, wheel_dim),
        ]