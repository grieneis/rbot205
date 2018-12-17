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
STANDARD_REWARD = -0.01
HOLE_REWARD = -1
BORDER_REWARD = -1000
IN_PLACE_REWARD = 0
MAX_REWARD = 1
GAMMA = 1.0

def iterate(val_in, reward):
    # val_in is a 2d array
    # initialize a new array of the same size
    val_out = np.zeros(val_in.shape)
    policy_out = np.ones(val_in.shape) * -1

    max_i = val_in.shape[0]
    max_j = val_in.shape[1]
    
    for i in range(1, max_i - 1):
        for j in range(1, max_j - 1):
            
            # the new value is the max over the 4 possible control actions
            val = float('-inf')
            
            # Caculate the raw values around the robot
            val_stay = val_in[i, j]
            val_up = val_in[i - 1, j] if reward[i - 1, j] != BORDER_REWARD else val_stay
            val_down = val_in[i + 1, j] if reward[i + 1, j] != BORDER_REWARD else val_stay
            val_left = val_in[i, j - 1] if reward[i, j - 1] != BORDER_REWARD else val_stay
            val_right = val_in[i, j + 1] if reward[i, j + 1] != BORDER_REWARD else val_stay
            
#            r_up = reward[i - 1, j] if reward[i - 1, j] != BORDER_REWARD else IN_PLACE_REWARD
#            r_down = reward[i + 1, j] if reward[i + 1, j] != BORDER_REWARD else IN_PLACE_REWARD
#            r_left = reward[i, j - 1] if reward[i, j - 1] != BORDER_REWARD else IN_PLACE_REWARD
#            r_right = reward[i, j + 1] if reward[i, j + 1] != BORDER_REWARD else IN_PLACE_REWARD

            r_here = reward[i, j]

#            val_up += r_up
#            val_down += r_down
#            val_left += r_left
#            val_right += r_right
            
            # test up
            prob_up = val_up * PROB_DESIRED \
                + val_down * PROB_BACK \
                + val_left * PROB_OFF \
                + val_right * PROB_OFF
            vf_up = prob_up #r_up + prob_up
            if vf_up > val:
                val = vf_up
                policy = 0
                
            prob_down = val_up * PROB_BACK \
                + val_down * PROB_DESIRED \
                + val_left * PROB_OFF \
                + val_right * PROB_OFF
            vf_down = prob_down # r_down + prob_down
            if vf_down > val:
                val = vf_down
                policy = 1
            
            prob_left = val_up * PROB_OFF \
                + val_down * PROB_OFF \
                + val_left * PROB_DESIRED \
                + val_right * PROB_BACK
            vf_left = prob_left #r_left + prob_left
            if vf_left > val:
                val = vf_left
                policy = 2
                
            prob_right = val_up * PROB_OFF \
                + val_down * PROB_OFF \
                + val_left * PROB_BACK \
                + val_right * PROB_DESIRED
            vf_right = prob_right #r_right + prob_right
            if vf_right > val:
                val = vf_right
                policy = 3
                    
              
            if r_here == MAX_REWARD or r_here == HOLE_REWARD:
                val = 0
                policy = 4
            if r_here == BORDER_REWARD:
                val = 0
                policy = 4
                r_here = 0

            val_out[i, j] =  GAMMA * val + r_here
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
    max_i = val.shape[0]
    max_j = val.shape[1]
    for i in range(max_i):
        for j in range(max_j): 
            if policy is not None:
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
                elif policy_val == 4:
                    character = 'o'
            else:
                character = '{0:.2f}'.format(val[i, j])
            ax.text(j - 0.3, i + 0.3, character, 
                    size='10', color='k', backgroundcolor='w')


# Create the intial arrays
#reward = np.ones((8, 20)) * -1
#reward[GOAL] = MAX_REWARD
#reward[4, 4:12] = HOLE_REWARD
#reward[4:8, 4:12] = HOLE_REWARD  
reward = np.ones((5, 6)) * STANDARD_REWARD

reward[1, 4] = 1
reward[2, 4] = -1
reward[2, 2] = BORDER_REWARD

reward[:, 0] = BORDER_REWARD
reward[:, -1] = BORDER_REWARD
reward[0, :] = BORDER_REWARD
reward[-1, :] = BORDER_REWARD



printArray(reward)

val_old = np.ones(reward.shape) * 0
policy = None
#printArray(val_old)
#print("Going to iterate")
iteration = 0
while iteration < 1000:
    (val_new, policy) = iterate(val_old, reward)
    if compareArrays(val_old, val_new):
        print("Made it at iteration {}".format(iteration))
        break
    val_old = val_new
    displayValuesAndControlPolicy(val_old)
    iteration += 1
#    printArray(val_old)
#    printArray(policy)
printArray(val_old)
printArray(policy)

displayValuesAndControlPolicy(val_old)
displayValuesAndControlPolicy(val_old, policy)