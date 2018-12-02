#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

def plot_data():
  # Generate some dummy controller data for plotting purposes
  # Create a vector of 20 samples evenly spaced data from -1 to 1
  t = np.linspace(-1, 1, 20)
  
  # Create a unit step at t = 0
  step = np.heaviside(t, 0)

  # Create an exponential response
  response = [1 - np.exp(-5*(m)) if m > 0 else 0 for m in t]

  # Plot the data
  plt.plot(t, step, 'b*--', label='input')
  plt.plot(t, response, 'ko-', label='response')

  # Add x and y labels
  plt.xlabel('Time [s]')
  plt.ylabel('Velocity [m/s]')

  # Add a title and the legend
  plt.title('Velocity response to a step input')
  plt.legend()

  # Save the plot as a png
  plt.savefig('sample.png')

  # Display the plot
  plt.show()

if __name__ == '__main__':
  plot_data()