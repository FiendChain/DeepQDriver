import numpy as np

from src.Environment import Environment

class WrapEnvironment(Environment):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
    
    def step(self, action, *args, **kwargs):
        action = self.controller(action)
        rv = super().step(action, *args, **kwargs)
        return rv

def dqn_controls(idx):
    action = [1,0,0]
    if idx == 0:
        action[1] = 0.6
    elif idx == 1:
        action[2] = -1
    elif idx == 2:
        action[2] = 1
    return action