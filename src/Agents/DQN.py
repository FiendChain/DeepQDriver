from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten


def create_dqn_model(env):

    model = Sequential()
    model.add(Flatten(input_shape=(1,env.nb_observations)))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(env.nb_actions))
    model.add(Activation('linear'))

    return model

def dqn_controls(idx):
    action = [1,0,0]
    if idx == 0:
        action[1] = 0.6
    elif idx == 1:
        action[2] = -1
    elif idx == 2:
        action[2] = 1
    return action