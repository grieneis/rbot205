#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 17:52:12 2018

@author: daniel.grieneisen
"""

import numpy as np
from matplotlib import pyplot as plt

def readFromCSV(filename):
    with open(filename, 'r') as fn:
        result_array = []
        for line in fn.readline():
            split_line = line.split(',')
            try:
                row = []
                for val in split_line:
                    row.append(np.float(split_line[0]))
                result_array.append(row)
            except:
                # Could not covert some data into floating point values
                # Skip this row
                continue
        return np.array(result_array)

def writeToCSV(filename, data):
    with open(filename, 'w') as fn:
        fn.write('x, y\n');
        for sample in data:
            fn.write('{}, {}\n'.format(data[0], data[1]))
            
def plotData(data):
    fig, ax = plt.subplots()
    ax.plot(data[..., 0], data[..., 1], '*', linewidth=2, color='firebrick')
    plt.title('Data')
    plt.xlabel('x value')
    plt.ylabel('y value')
    

def generateData(fn, min_x, max_x):
    output = []
    x = np.linspace(min_x, max_x, 100)
    for val in x:
        output.append([val, fn(val)])
    return np.array(output)

def random_val(val):
    return np.random.uniform(-val, val)

def fn1(x):
    return 5 + 1.5 * x - 0.2 * x * x + random_val(0.75)

def fn2(x):
    return 0.25 * np.exp(x) + 1.0 / x + random_val(4)

def fn3(x):
    return 1.4 * np.cos(x) + + 0.5 * x + random_val(2.0)

data1 = generateData(fn1, 0, 5)
data2 = generateData(fn2, 0.1, 5)
data3 = generateData(fn3, -np.pi * 2, np.pi * 2)

plotData(data1)
plotData(data2)
plotData(data3)

writeToCSV('ols_1.csv', data1)
writeToCSV('ols_2.csv', data2)
writeToCSV('ols_3.csv', data3)