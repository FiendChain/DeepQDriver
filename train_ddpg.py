from src.Environment import *
import pickle
import time
import os
from argparse import ArgumentParser

def train_agent(env, args):
    from src.Agents import create_ddpg_actor, create_ddpg_critic, ddpg_controls, EnvironmentWrapper
    from keras.optimizers import Adam

    from rl.agents.ddpg import DDPGAgent
    from rl.policy import EpsGreedyQPolicy
    from rl.memory import SequentialMemory
    from rl.random import OrnsteinUhlenbeckProcess

    env = EnvironmentWrapper(ddpg_controls, env) 

    nb_actions = 3
    actor = create_ddpg_actor(env)
    critic, action_input = create_ddpg_critic(env)

     # Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
    # even the metrics!
    memory = SequentialMemory(limit=100000, window_length=1)
    random_process = OrnsteinUhlenbeckProcess(size=nb_actions, theta=.15, mu=0., sigma=.3)
    agent = DDPGAgent(nb_actions=nb_actions, actor=actor, critic=critic, critic_action_input=action_input,
                    memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=100,
                    random_process=random_process, gamma=.99, target_model_update=1e-3)
    agent.compile(Adam(lr=.001, clipnorm=1.), metrics=['mae'])

    try:
        agent.load_weights(args.ai_in)
    except OSError:
        pass

    # Okay, now it's time to learn something! We visualize the training here for show, but this
    # slows down training quite a lot. You can always safely abort the training prematurely using
    # Ctrl + C.
    agent.fit(env, nb_steps=20000, visualize=False, verbose=2)

    # After training is done, we save the final weights.
    agent.save_weights(args.ai_out, overwrite=True)

    # Finally, evaluate our algorithm for 5 episodes.
    agent.test(env, nb_episodes=5, visualize=False)


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
    sensor = Sensor(170)
    env = Environment(car, sensor, M)

    train_agent(env, args)

    env.on_exit()

if __name__ == '__main__':
    main()

