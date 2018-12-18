#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 13:15:18 2018

@author: daniel.grieneisen
"""
import numpy as np
import matplotlib.pyplot as plt


def valueIterate(val_in, reward):
    # val_in is a 2d array
    # initialize a new array of the same size
    val_out = np.zeros(val_in.shape)
    policy_out = np.ones(val_in.shape) * -1
    
    return (val_out, policy_out)


# Check to see if all of the values are the same in the two arrays
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
    
def displayArray(val, policy=None, title='', save=False):
    fig, ax = plt.subplots()
    ax.imshow(val, cmap = plt.get_cmap('gray'))
    max_i = val.shape[0]
    max_j = val.shape[1]
    for i in range(max_i):
        for j in range(max_j):
            character = ''
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
            elif val[i, j] != 0.0 and val[i, j] != BORDER_REWARD:
                character = '{0:.1f}'.format(val[i, j])
            ax.text(j - 0.3, i + 0.3, character, 
                    size='10', color='k', backgroundcolor='w')
    plt.xlabel('x position')
    plt.ylabel('y position')
    plt.title(title+' Gamma: {}, P(correct): {}'.format(GAMMA, PROB_DESIRED))
    if save:
        plt.savefig('chart_'+str(PROB_DESIRED)+'_'+str(GAMMA)+'_'+title+'.png')
        



# Create the reward array
STANDARD_REWARD = -1
HOLE_REWARD = -100
BORDER_REWARD = -1000
GOAL_REWARD = 100

# Initialize the array
reward = np.ones((5, 6)) * STANDARD_REWARD

# Insert the goal and hole
reward[1, 4] = GOAL_REWARD
reward[2, 4] = HOLE_REWARD
reward[2, 2] = BORDER_REWARD


# Add borders
reward[:, 0] = BORDER_REWARD
reward[:, -1] = BORDER_REWARD
reward[0, :] = BORDER_REWARD
reward[-1, :] = BORDER_REWARD


# Show the reward array
printArray(reward)
displayArray(reward, None, 'reward', True)

val_old = np.ones(reward.shape) * 0
policy = None

iteration = 0
while iteration < 1000:
    (val_new, policy) = valueIterate(val_old, reward)
    if compareArrays(val_old, val_new):
        print("Finished at iteration {}".format(iteration))
        break
    val_old = val_new
    iteration += 1

printArray(val_old)
printArray(policy)

displayArray(val_old, None, 'final_value', True)
displayArray(val_old, policy, 'policy', True)