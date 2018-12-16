#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 13:15:18 2018

@author: daniel.grieneisen
"""
import numpy as np
import matplotlib.pyplot as plt

# create the map
PROB_DESIRED = 1.0
PROB_OFF = (1 - PROB_DESIRED) / 2
PROB_BACK = 0
HOLE_REWARD = -100
GAMMA = 1.0
MAX_REWARD = 100
GOAL = (5, 2)

def iterate(val_in, reward):
    # val_in is a 2d array
    # initialize a new array of the same size
    val_out = np.zeros(val_in.shape)
    policy_out = np.ones(val_in.shape) * -1

    max_i = val_in.shape[0]
    max_j = val_in.shape[1]
    
    for i in range(max_i):
        for j in range(max_j):
            
            # the new value is the max over the 4 possible control actions
            val = float('-inf')
            # test up
            if i > 0:
                r = reward[i - 1, j]
                prob_up = val_in[i - 1, j] * PROB_DESIRED
                prob_left = val_in[i, j - 1] * PROB_OFF if j > 0 else 0
                prob_right = val_in[i, j + 1] * PROB_OFF if j < max_j - 1 else 0
                prob_down = val_in[i + 1, j] * PROB_BACK if i < max_i - 1 else 0
                val_up = r + prob_up + prob_left + prob_right + prob_down
                if val_up > val:
                    val = val_up
                    policy = 0
            else:
                # bumped off of wall?
                pass
            # test down
            if i < max_i - 1:
                r = reward[i + 1, j]
                prob_up = val_in[i - 1, j] * PROB_BACK
                prob_left = val_in[i, j - 1] * PROB_OFF if j > 0 else 0
                prob_right = val_in[i, j + 1] * PROB_OFF if j < max_j - 1 else 0
                prob_down = val_in[i + 1, j] * PROB_DESIRED if i < max_i - 1 else 0
                val_down = r + prob_up + prob_left + prob_right + prob_down
                if val_down > val:
                    val = val_down
                    policy = 1
                    
            # test left
            if j > 0:
                r = reward[i, j - 1]
                prob_up = val_in[i - 1, j] * PROB_OFF
                prob_left = val_in[i, j - 1] * PROB_DESIRED if j > 0 else 0
                prob_right = val_in[i, j + 1] * PROB_BACK if j < max_j - 1 else 0
                prob_down = val_in[i + 1, j] * PROB_OFF if i < max_i - 1 else 0
                val_left = r + prob_up + prob_left + prob_right + prob_down
                if val_left > val:
                    val = val_left
                    policy = 2
            # test right
            if j < max_j - 1:
                r = reward[i, j + 1]
                prob_up = val_in[i - 1, j] * PROB_OFF
                prob_left = val_in[i, j - 1] * PROB_BACK if j > 0 else 0
                prob_right = val_in[i, j + 1] * PROB_DESIRED if j < max_j - 1 else 0
                prob_down = val_in[i + 1, j] * PROB_OFF if i < max_i - 1 else 0
                val_right = r + prob_up + prob_left + prob_right + prob_down
                if val_right > val:
                    val = val_right
                    policy = 3
                    
#            if reward[i, j] == MAX_REWARD or reward[i, j] == HOLE_REWARD:
#                val = reward[i, j]
            val_out[i, j] = GAMMA * val
            policy_out[i, j] = policy
    return (val_out, policy_out)

def compareArrays(old_arr, new_arr):
    max_i = old_arr.shape[0]
    max_j = old_arr.shape[1]
    
    for i in range(max_i):
        for j in range(max_j):
            if np.fabs(old_arr[i, j] - new_arr[i, j]) > 0.001:
                return False
    return True
def printArray(arr):
    print("{}".format(arr))
    
def displayValuesAndControlPolicy(val, policy=None):
    fig, ax = plt.subplots()
    ax.imshow(val, cmap = plt.get_cmap('gray'))
    if policy is not None:
        max_i = policy.shape[0]
        max_j = policy.shape[1]
        for i in range(max_i):
            for j in range(max_j):    
                character = ''
                policy_val = policy[i, j]
                if policy_val == 0:
                    character = '^'
                elif policy_val == 1:
                    character = 'v'
                elif policy_val == 2:
                    character = '<'
                elif policy_val == 3:
                    character = '>'
                ax.text(i - 0.15, j + 0.15, character, size='20', color='r')


# Create the intial arrays
#reward = np.ones((8, 20)) * -1
#reward[GOAL] = MAX_REWARD
#reward[4, 4:12] = HOLE_REWARD
#reward[4:8, 4:12] = HOLE_REWARD  
reward = np.ones((5, 5)) * -1
reward[(2, 2)] = MAX_REWARD
#reward[1:, 0] = HOLE_REWARD

#printArray(reward)

val_old = np.ones(reward.shape) * -1
policy = None
#printArray(val_old)
#print("Going to iterate")
iteration = 0
while iteration < 1000:
    (val_new, policy) = iterate(val_old, reward)
    if compareArrays(val_old, val_new):
        print("Made it at iteration {}".format(iteration))
        print(val_new)
        break
    val_old = val_new
    iteration += 1
    printArray(val_old)
printArray(val_old)

displayValuesAndControlPolicy(val_old, policy)