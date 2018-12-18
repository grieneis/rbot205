#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 13:15:18 2018

@author: daniel.grieneisen
"""
import numpy as np
import matplotlib.pyplot as plt

# create the map
PROB_DESIRED = 0.8
PROB_OFF = (1 - PROB_DESIRED) / 2
PROB_BACK = 0
STANDARD_REWARD = -1
HOLE_REWARD = -100
BORDER_REWARD = -1000
IN_PLACE_REWARD = 0
MAX_REWARD = 100
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
            

            val_array = np.array([val_up, val_down, val_left, val_right])
            
            vf_up = np.dot(val_array, 
                           np.array([PROB_DESIRED, PROB_BACK, PROB_OFF, PROB_OFF]))
            vf_down = np.dot(val_array, 
                           np.array([PROB_BACK, PROB_DESIRED, PROB_OFF, PROB_OFF]))
            vf_left = np.dot(val_array, 
                           np.array([PROB_OFF, PROB_OFF, PROB_DESIRED, PROB_BACK]))
            vf_right = np.dot(val_array, 
                           np.array([PROB_OFF, PROB_OFF, PROB_BACK, PROB_DESIRED]))
            
            vf_array = np.array([vf_up, vf_down, vf_left, vf_right])
            
            policy = np.argmax(vf_array)
            val = np.max(vf_array)
            
            r_here = reward[i, j]

              
            if r_here == MAX_REWARD or r_here == HOLE_REWARD:
                val = 0
                policy = 4
            if r_here == BORDER_REWARD:
                val = 0
                policy = -1
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
        


# Create the intial arrays
#reward = np.ones((8, 20)) * -1
#reward[GOAL] = MAX_REWARD
#reward[4, 4:12] = HOLE_REWARD
#reward[4:8, 4:12] = HOLE_REWARD  
reward = np.ones((8, 13)) * STANDARD_REWARD
reward[4, 3:8] = HOLE_REWARD
reward[6:7, 3:8] = HOLE_REWARD 

reward[5, 1] = MAX_REWARD
#reward[2, 4] = HOLE_REWARD
#reward[2, 2] = BORDER_REWARD

reward[:, 0] = BORDER_REWARD
reward[:, -1] = BORDER_REWARD
reward[0, :] = BORDER_REWARD
reward[-1, :] = BORDER_REWARD



printArray(reward)

displayArray(reward, None, 'reward', True)

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
    if iteration <= 3:
#        displayArray(val_old, None, 'value-at-'+str(iteration), True)
        pass

#    displayValuesAndControlPolicy(val_old)
    iteration += 1
#    printArray(val_old)
#    printArray(policy)
printArray(val_old)
printArray(policy)

#displayArray(val_old, None, 'final_value', True)
#displayArray(val_old, policy, 'policy', True)