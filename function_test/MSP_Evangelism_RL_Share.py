#
# get_ipython().system(u'python3.6 -m pip install gym[all]')

import gym
import numpy as np
import random
import math
import random

import matplotlib
import matplotlib.pyplot as plt

# ### Load OpenAI Gym (\*TODO\*)
""" Code Start """

# Load OpenAI Gym's Environment
# Environment title 'CartPole-v0'
env = gym.make('CartPole-v0')

# Modify environment to expand steps(500) at each episode
env._max_episode_steps = 500

""" Code End """


# Number of discrete states (bucket) per state dimension
NUM_BUCKETS = (1, 1, 6, 3)  # (x, x', theta, theta')
#저장소가 가지는 범위

# Number of discrete actions
NUM_ACTIONS = env.action_space.n # (left, right)

# Bounds for each discrete state
STATE_BOUNDS = list(zip(env.observation_space.low, env.observation_space.high))
STATE_BOUNDS[1] = [-0.5, 0.5]
STATE_BOUNDS[3] = [-math.radians(50), math.radians(50)]

# Index of the action
ACTION_INDEX = len(NUM_BUCKETS)


# ### Defining the Q-learning related constants(\*TODO\*)



""" Code Start """

## Creating a Q-Table for each state-action pair
q_table =  np.zeros(NUM_BUCKETS + (NUM_ACTIONS,))

num_streaks = 0
record = []

## Defining the Learning related constants
MIN_EXPLORE_RATE = 0.01
MIN_LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.99

## Defining the simulation related constants
MAX_EPISODES = 1000
MAX_STEPS = 550
SOLVED_STEPS = 499
STREAK_TO_END = 120

""" Code End """


# # Implement Sub-modules

# ### Get learning related values at the given time t

# Decreasing exploring rate over time t
def get_explore_rate(t):
    if t >= 24:
        # Does not decreas below the MIN_EXPLORE_RATE
        return max(MIN_EXPLORE_RATE, min(1, 1.0 - math.log10((t+1)/25)))
    else:
        return 1.0

# Decreasing learning rate over time t
def get_learning_rate(t):
    if t >= 24:
        # Does not decreas below the MIN_LEARNING_RATE
         return max(MIN_LEARNING_RATE, min(0.5, 1.0 - math.log10((t+1)/25)))
    else:
         return 1.0


# ### Get the most proper action at the given state

def select_action(state, explore_rate):
    """ Code Start """
    
    # Select a random action : Epsilon-greedy
    if random.random() < explore_rate:
        action = env.action_space.sample()
        
    # Select the action with the highest q
    else:
        action = np.argmax(q_table[state])
        
    """ Code End """
    return action


# ### Convert observation to state

def observation_to_state(observation):
    state = []
    for i in range(len(observation)):
        if observation[i] <= STATE_BOUNDS[i][0]:
            bucket_index = 0
        elif observation[i] >= STATE_BOUNDS[i][1]:
            bucket_index = NUM_BUCKETS[i] - 1
        else:
            # Mapping the state bounds to the bucket array
            bound_width = STATE_BOUNDS[i][1] - STATE_BOUNDS[i][0]
            offset = (NUM_BUCKETS[i]-1)*STATE_BOUNDS[i][0]/bound_width
            scaling = (NUM_BUCKETS[i]-1)/bound_width
            bucket_index = int(round(scaling*observation[i] - offset))
        state.append(bucket_index)
    return tuple(state)


# # Simulate Q-Learning

def simulate():
    num_streaks = 0

    for episode in range(MAX_EPISODES):
        """ Code Start """
        
        # Initiate learning related values
        explore_rate = get_explore_rate(episode)
        learning_rate = get_learning_rate(episode)
        
        """ Code End """
        
        # Reset the environment
        obv = env.reset()
        state_prev = observation_to_state(obv)

        for step in range(MAX_STEPS):
            """ Code Start """
            
            # Select an action
            action = select_action(state_prev, explore_rate)

            # Execute the action
            obv, reward, done, _ = env.step(action)

            # Observe the result
            state_next = observation_to_state(obv)

            # Update the Q based on the result
            best_q = np.amax(q_table[state_next])
            q_table[state_prev + (action,)] += learning_rate * (reward + DISCOUNT_FACTOR * best_q - q_table[state_prev + (action,)])
            
            """ Code End """
            # Setting up for the next iteration
            state_prev = state_next
            
            if done:
               record.append(step)
               print("Episode %d finished after %f time steps" % (episode, step))
               if (step >= SOLVED_STEPS):
                   num_streaks += 1
               else:
                   num_streaks = 0
               break

        # It's considered done when it's solved over STREAK_TO_END times consecutively
        if num_streaks > STREAK_TO_END:
            break


# # Visualize time-reward Graph
def visualize():
    for i_episode in range(20):
        observation = env.reset()  # reset for each new trial
        for t in range(100):  # run for 100 timesteps or until done, whichever is first
            env.render()
            action = env.action_space.sample()  # select a random action (see https://github.com/openai/gym/wiki/CartPole-v0)
            observation, reward, done, info = env.step(action)
            if done:
                print("Episode finished after {} timesteps".format(t + 1))
                break

# # Let's Start!

if __name__ == "__main__":
    simulate()
    visualize()

