from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate

def create_ddpg_actor(env):
    # Next, we build a very simple model.
    actor = Sequential()
    actor.add(Flatten(input_shape=(1,env.nb_observations)))
    actor.add(Dense(16))
    actor.add(Activation('relu'))
    actor.add(Dense(16))
    actor.add(Activation('relu'))
    actor.add(Dense(16))
    actor.add(Activation('relu'))
    actor.add(Dense(env.nb_actions))
    actor.add(Activation('sigmoid'))

    print(actor.summary())

    return actor

def create_ddpg_critic(env):
    action_input = Input(shape=(env.nb_actions,), name='action_input')
    observation_input = Input(shape=(1,env.nb_observations), name='observation_input')

    flattened_observation = Flatten()(observation_input)
    x = Concatenate()([action_input, flattened_observation])
    x = Dense(32)(x)
    x = Activation('relu')(x)
    x = Dense(16)(x)
    x = Activation('relu')(x)
    x = Dense(1)(x)
    x = Activation('linear')(x)
    critic = Model(inputs=[action_input, observation_input], outputs=x)
    print(critic.summary())

    return (critic, action_input)

def ddpg_controls(response):
    action = response
    action[0] = 1

    return action