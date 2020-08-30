class EnvironmentWrapper:
    def __init__(self, controller, env):
        self.env = env
        self.controller = controller
    
    def step(self, action, *args, **kwargs):
        action = self.controller(action)
        return self.env.step(action, *args, **kwargs)

    def reset(self):
        return self.env.reset()
    
    def on_exit(self):
        return self.env.on_exit()

    def get_observation(self):
        return self.env.get_observation()
        
    @property
    def car(self):
        return self.env.car

    @property
    def map(self):
        return self.env.map
    
    @property
    def sensor(self):
        return self.env.sensor

    @property
    def nb_observations(self):
        return self.env.nb_observations
    
    @property
    def nb_actions(self):
        return self.env.nb_actions