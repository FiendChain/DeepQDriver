from .Vec2D import Vec2D
import math

from .util import point_rot, clip, get_points


class Car:
    def __init__(self):
        self.dim = Vec2D(20, 35)

        self.reset()

        self.mass = 100

        self.F_engine_max = 8
        self.rev_rate = 0.05

        self.Cdrag = 0.3
        self.Crr = 0.7 # rolling resistance
        self.Cbrake = 4 

        self.Clateral = 2 # cornering stiffness

        self.wheel_angle_max = math.pi/6

        self.drift = True

        self.v_control = 4
        self.v_traction = 3.5
        self.C_drift_control = 0.4
        self.C_drift_traction = 0.5
        self.C_drift_sideslip = 0.3

        self.drift_factor = 0
    
    def reset(self):
        self.dir = 0
        self.pos = Vec2D(0, 0)
        self.vel = Vec2D(0, 0)
        self.rev = 0
        self.wheel = 0
        self.accel = 0
        self.brake = 0
        self.drift_factor = 0
    
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
        drift_vec = point_rot(self.vel, math.pi/2)
        drift_vec = drift_vec.norm()
        drift_angle_cos = drift_vec.dot(vel_norm)
        Frr_lat = -self.Crr*(1-self.rev)*(drift_vec*vel_len*drift_angle_cos)

        # turning
        wheel_angle = self.wheel*self.wheel_angle_max

        # drifting
        if self.drift:
            v_control = self.v_control
            v_traction = self.v_traction

            control_factor = clip(vel_len, 0, v_control)/v_control
            traction_factor = clip(vel_len, 0, v_traction)/v_traction


            wheel_control = (1-control_factor*self.C_drift_control)*clip(sideslip_angle_cos, self.C_drift_sideslip, 1)
            wheel_traction = (1-traction_factor*self.C_drift_traction)

            drift_vector = point_rot(vel_norm, -self.dir)
            self.drift_factor = drift_vector.x

            # print(f"{self.drift_factor:.2f}\r", end='')

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

            self.drift_factor = 0

        

        # sum forces
        Fnet = Ftraction + Fdrag + Frr + Fbrake + Fcorner + Frr_lat
        accel = Fnet/self.mass

        self.vel += accel*dt
        self.pos += self.vel*dt
    
    @property
    def nb_observations(self):
        return 1
    
    def get_observation(self):
        return [self.drift_factor]
    
    @property
    def nb_actions(self):
        return 3

    def set_action(self, action):
        accel, brake, wheel = action

        self.accel = clip(accel, 0, 1)
        self.brake = clip(brake, 0, 1)
        self.wheel = clip(wheel, -1, 1)
    
    def get_segments(self):
        body_points = get_points(self.pos, self.dir, self.dim)
        body_segments = list(zip(body_points[1:], body_points[:-1]))
        return body_segments



        