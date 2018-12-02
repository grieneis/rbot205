#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import time

def bubble_sort(data):
  print('Bubble sort not implemented')
  return data

def merge_sort(data):
  print('Merge sort not implemented')
  return data

def sort(algorithm, data):
  # Here is where you can implement your sorting algorithm
  if algorithm == 'BUBBLE':
    return bubble_sort(data)
  elif algorithm == 'MERGE':
    return merge_sort(data)
  else:
    print('Requested algorithm is not implemented')
    return data

def run_test():
  # Define some constants that we will use for running 
  algorithm = 'BUBBLE' # the algorithm to use
  max_int = 1000000 # the maximum size of an integer to sort
  num_samples = 1000 # the number of samples of data to sort
  num_iterations = 1000 # the number of times to run the sorting algorithm

  start_time = time.time();
  for x in range(0, num_iterations):
    unsorted_data = np.random.random_integers(0, max_int, num_samples)
    sorted_data = sort(algorithm, unsorted_data)
  end_time = time.time()
  total_time = end_time - start_time
  average_time = total_time / num_iterations

  print('Algorithm {} took {} seconds for {} iterations, or {} seconds per iteration.'.format(
    algorithm, total_time, num_iterations, average_time))

if __name__ == '__main__':
  run_test()