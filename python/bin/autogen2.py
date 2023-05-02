## Generated with ChatGPT

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import simpy

class Battery:
    def __init__(self, env, level):
        self.env = env
        self.level = level

# Define the battery depletion and recharging processes with temperature dependence
def battery_depletion(env, bat, temp):
    k_d = 0.1 * np.exp(-3000 / (8.314 * (temp + 273))) # Depletion rate constant
    while True:
        yield env.timeout(1) # Deplete the battery level by 1% every hour
        bat.level -= k_d
        if bat.level <= 0:
            bat.level = 0
            break

def battery_recharge(env, bat, temp):
    k_r = 1.5 * np.exp(-2000 / (8.314 * (temp + 273))) # Recharge rate constant
    while True:
        yield env.timeout(1) # Recharge the battery level by 1% every hour
        bat.level += k_r
        if bat.level >= 100:
            bat.level = 100
            break

# Set up the simulation environment and battery object
env = simpy.Environment()
bat = simpy.Container(env, init=100)

# Set up the temperature values
temp = np.linspace(10, 50, 41)

# Start the depletion and recharging processes for each temperature value
for tmp in temp:
    env.process(battery_depletion(env, bat, tmp))
    env.process(battery_recharge(env, bat, tmp + 5)) # Recharge at a slightly higher temperature

# Run the simulation for 100 hours
env.run(until=100)

# Plot the battery level over time and temperature
plt.imshow(bat.level.T, origin='lower', aspect='auto', cmap='viridis',
           extent=[0, 100, temp[0], temp[-1]], vmin=0, vmax=100)
plt.xlabel('Battery Level (%)')
plt.ylabel('Temperature (Celsius)')
plt.colorbar(label='Battery Level (%)')
plt.show()
