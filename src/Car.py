from .Vec2D import Vec2D
import math

from .util import point_rot, clip


class Car:
    def __init__(self):
        self.dim = Vec2D(20, 35)

        self.dir = 0 # radians

        self.pos = Vec2D(0,0)
        self.vel = Vec2D(0,0)

        self.mass = 100

        self.F_engine_max = 5
        self.rev_rate = 0.05
        self.rev = 0

        self.Cdrag = 0.3
        self.Crr = 0.7 # rolling resistance
        self.Cbrake = 4 

        self.Clateral = 2 # cornering stiffness


        self.wheel = 0
        self.wheel_angle_max = math.pi/6

        self.accel = 0
        self.brake = 0
    
    def tick(self, dt=1):
        dir_vec = point_rot(Vec2D(0,1), self.dir)
        vel_len = self.vel.length()
        vel_norm = self.vel.norm()

        sideslip_angle_cos = dir_vec.dot(vel_norm)

        if self.accel > 0:
            self.rev = clip(self.rev+self.rev_rate*self.accel, 0, 1)
        else:
            self.rev = clip(self.rev-self.rev_rate, 0, 1)

        F_engine_mag = self.F_engine_max*self.rev

        # longitudinal motion
        Ftraction = dir_vec*F_engine_mag
        Fbrake = -self.Cbrake*self.brake*(dir_vec*vel_len*sideslip_angle_cos)
        Fdrag = -self.Cdrag*self.vel*vel_len
        Frr = -self.Crr*self.vel

        # latitude motion
        # we scale drifting drag with engine power
        drift_vec = point_rot(dir_vec, math.pi/2)
        drift_angle_cos = drift_vec.dot(vel_norm)
        Frr_lat = -self.Crr*(1-self.rev)*(drift_vec*vel_len*drift_angle_cos)

        # turning
        wheel_angle = self.wheel*self.wheel_angle_max

        # drifting
        drift = False
        if drift:
            v_control = 4
            v_traction = 1.5

            control_factor = clip(vel_len, 0, v_control)/v_control
            traction_factor = clip(vel_len, 0, v_traction)/v_traction


            wheel_control = (1-control_factor*0.5)*clip(sideslip_angle_cos, 0.2, 1)
            wheel_traction = (1-traction_factor*0.9)

            # compute forces and rotation
            R_inv = math.sin(wheel_angle * wheel_control)/self.dim.y # turn radius
            omega = vel_len*R_inv

            F_corner_mag = self.mass*(vel_len**2)*R_inv
            F_corner_dir = point_rot(Vec2D(0,1), self.dir+wheel_angle+math.pi/2)

            Fcorner = F_corner_mag * F_corner_dir * wheel_traction

            self.dir += omega*dt
        else:
            wheel_angle = self.wheel*self.wheel_angle_max
            R_inv = math.sin(wheel_angle)/self.dim.y # turn radius
            omega = vel_len*R_inv

            F_corner_mag = self.mass*(vel_len**2)*R_inv
            F_corner_dir = point_rot(Vec2D(0,1), self.dir+wheel_angle+math.pi/2)

            Fcorner = F_corner_mag * F_corner_dir
            self.dir += omega*dt

        

        # sum forces
        Fnet = Ftraction + Fdrag + Frr + Fbrake + Fcorner + Frr_lat
        accel = Fnet/self.mass

        self.vel += accel*dt
        self.pos += self.vel*dt
        

    def set_accelerator(self, x):
        self.accel = clip(x, 0, 1)
    
    def set_brake(self, x):
        self.brake = clip(x, 0, 1)
    
    def set_wheel(self, x):
        self.wheel = clip(self.wheel+x, -1, 1)

        