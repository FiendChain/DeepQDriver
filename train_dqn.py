from src.Environment import *
import pickle
import time
import os
from argparse import ArgumentParser

def train_dqn(env, args):
    from src.Agents import create_dqn_model, dqn_controls, EnvironmentWrapper
    from keras.optimizers import Adam

    from rl.agents.dqn import DQNAgent
    from rl.policy import EpsGreedyQPolicy
    from rl.memory import SequentialMemory

    env = EnvironmentWrapper(dqn_controls, env) 

    model = create_dqn_model(env)

    memory = SequentialMemory(limit=50000, window_length=1)
    policy = EpsGreedyQPolicy()
    dqn = DQNAgent(model=model, nb_actions=env.nb_actions, memory=memory, nb_steps_warmup=2000,
                target_model_update=1e-2, policy=policy)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    try:
        dqn.load_weights(args.ai_in)
    except OSError:
        pass

    dqn.fit(env, nb_steps=50000, visualize=False, verbose=2)
    dqn.save_weights(args.ai_out, overwrite=True)
    dqn.test(env, nb_episodes=1, visualize=False)


def main():
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
    car.C_drift_control = 0.3
    car.C_drift_traction = 0.4
    car.C_drift_sideslip = 0.3
    # car.F_engine_max = 10
    car.F_engine_max = 8

    # sensor = Sensor(300, total=16)
    sensor = NonLinearSensor(300, total=16)
    env = Environment(car, sensor, M)

    train_dqn(env, args)

    env.on_exit()

if __name__ == '__main__':
    main()


