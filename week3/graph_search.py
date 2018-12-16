# -*- codi utf-8 -*-
"""
Code to get started exploring graph search.
"""

import numpy as np
import matplotlib.pyplot as plt

# Convert an rgb image to greyscale
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

# Read in the map and return it as a 2d array where 1 is clear and 0 is occupied
def read_world_image(path):
    img = plt.imread(path)
    return rgb2gray(img)

def plot_results(world, path, explored_cells):
    fig, ax = plt.subplots()
    ax.imshow(world, cmap = plt.get_cmap('gray'))
    ax.plot(path, '-.', linewidth=2, color='firebrick')
    ax.plot(explored_cells, '*', color='blue')
    plt.title('TITLE HERE')
    plt.xlabel('X LABEL')
    plt.ylabel('Y LABEL')
    
    
def plan_path(world):
    # Path planner code goes here.
    
    # path should be an array of the form [[x1, y1], .. [xn, yn]]
    # containing the path produced by your planner.
    path = [[1, 2], [2, 3], [3, 4]] # dummy example
    
    # explored_cells should an array of the form [[x1, y1], .. [xn, yn]]
    # containing the indices of all cells explored by the planner.
    explored_cells = [[1, 3], [6, 3], [10, 4]] # dummy example
    
    return (path, explored_cells)

# Read the map
# Replace the file path with the location on your computer where you saved the map
file_path = '/Users/daniel.grieneisen/Documents/teaching/rbot205/week3/map.png'
world = read_world_image(file_path)

## Plan a path
(path, explored_cells) = plan_path(world)

plot_results(world, path, explored_cells)


