import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

## Generated with ChatGPT

# Define the function that models the battery depletion over time
def battery(t, a, b, c):
    return a * np.exp(-b * t) + c 

# Set the initial parameters for the battery model
a = 100  # initial charge (mAh)
b = 0.01  # discharge rate (per hour)
c = 0  # final charge (mAh)

# Create a time array for the simulation
t = np.linspace(0, 24, 100)

# Simulate the battery depletion over time
charge = battery(t, a, b, c)

# Plot the results
plt.plot(t, charge)
plt.xlabel('Time (hours)')
plt.ylabel('Charge (mAh)')
plt.title('Battery Depletion Over Time')
plt.show()
