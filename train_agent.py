from src import Car, Map, Environment, Sensor
import pickle
import time
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("map_file")
parser.add_argument("ai_in")
parser.add_argument("ai_out")
parser.add_argument("--override", action="store_true")

args = parser.parse_args()

if os.path.isfile(args.ai_out) and not args.override:
    print(f"Cannot override output {args.out_file}")
    exit()

with open(args.map_file, "rb") as fp:
    M = pickle.load(fp)

car = Car()
sensor = Sensor(170)
env = Environment(car, sensor, M)

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

nb_actions = 3

model = Sequential()
model.add(Flatten(input_shape=(1,8)))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))

print(model.summary())


memory = SequentialMemory(limit=50000, window_length=1)
policy = EpsGreedyQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=1000,
               target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=0.5e-2), metrics=['mae'])
dqn.load_weights(args.ai_in)

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
dqn.fit(env, nb_steps=20000, visualize=False, verbose=2)

# After training is done, we save the final weights.
dqn.save_weights(args.ai_out, overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=5, visualize=False)


