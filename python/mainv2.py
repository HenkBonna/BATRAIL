import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import scipy as sp
import matplotlib.gridspec as gridspec

###########################################################
####  PLOT STUFF ####################################### 

gs = gridspec.GridSpec(nrows=3, ncols=2, width_ratios=[1, 1.5], height_ratios=[1, 1, 1.25])

# Create the three axes
fig = plt.figure("BATRAIL", constrained_layout=True, figsize=(12, 7))

# Define Graph axes
ax_temp = fig.add_subplot(gs[0, 0]) 
ax_charge = fig.add_subplot(gs[1, 0]) 
ax_info_1 = fig.add_subplot(gs[2, 0]) 
ax_info_2 = fig.add_subplot(gs[2, 1]) 
ax_main = fig.add_subplot(gs[0:2, 1])

ax_info_1.axis('off')
ax_info_2.axis('off')
props = dict(boxstyle='square', facecolor='white', alpha=0.5)

###########################################################
####  MODELLING STUFF ####################################### 

class Environment():
    def __init__(self, name, altitude, temperature_lists):
        self.name = name
        self.altitude = altitude
        self.temperature_lists = temperature_lists

class Machine():
    def __init__(self, name, weight, battery, consumption):
        self.name = name
        self.weight = weight
        self.battery = battery
        self.consumption = consumption
        
class Battery():
    def __init__(self, name, capacity, charge_rate, weight):
        self.name = name
        self.capacity = capacity
        self.charge_rate = charge_rate
        self.weight = weight
        # Temperature dependency

# Nested temperature control should affect the battery
# Perhaps model the box around the battery

def simulato(duration, List_Of_Machines, Environment):
    e = Environment
    time_list = np.arange(0, duration, 1, dtype=int)
    temp_profiles = []
    for temps in e.temperature_lists:
        temp_profile = expand_array(np.array(temps), duration)
        temp_profiles.append(temp_profile)

    #temp_list = temp
    charge_lists = []

    list_of_results = []
    for i in range(len(List_Of_Machines)):
        if len(List_Of_Machines)!=len(temp_profiles): # Ensure conforming, otherwise only 1 temp profile is used
            temp_list = temp_profiles[0]
        else:
            temp_list = temp_profiles[i]
        b = List_Of_Machines[i].battery
        capacity = 0.95 *b.capacity 
        result = []
        # Running the simulation
        t = 0
        charging = False
        temps = []
        charge_list = []
        while t<duration:
            result.append(capacity)
            chrg = 0
            if capacity < 0.1*b.capacity: 
                charging = True
            if charging == True:
                chrg = chargo(10*b.charge_rate, temp_list[t])
                capacity = capacity + chrg # TODO: Fix this
                if capacity > 0.95*b.capacity:
                    charging = False
            else:
                capacity = capacity - depleto((List_Of_Machines[i].consumption/60),temp_list[t]) # TODO: Fix this

            if(capacity<0):
                capacity=0
            #elif(capacity>1000):
            #    capacity=1000


            charge_list.append(chrg)
            t = t+1
        list_of_results.append(result)
        charge_lists.append(charge_list)

    # Create the plot

    # Subgraphs
    ax_temp.set(ylabel='Temperature [C]')
    #ax_charge.plot(time_list,charge_list, 'tab:green')
    ax_charge.set(xlabel='Time [min]', ylabel='Charging rate')

    # Main Graph
    col='tab:green'
    for i in range(len(list_of_results)):
        col = cycle_col(col)
        # Plot all temps
        if len(List_Of_Machines)!=len(temp_profiles): # Ensure conforming, otherwise only 1 temp profile is used
            ax_temp.plot(time_list,temp_profiles[0], col)
        else:
            ax_temp.plot(time_list,temp_profiles[i], col)
        # Plot all depletions
        ax_main.plot(time_list,list_of_results[i], col) # TODO: The m and b values are after assigning
        ax_charge.plot(time_list, charge_lists[i], col)
    ax_main.set(xlabel='Time [min]', ylabel='Capacity [kWh]')

# A very rough way of caluclating depletion-variation with temperature.
def depleto(consumption, temperature):
    temp_coeff = 1.00
    if temperature < -35:
        temp_coeff = 4.00
    elif temperature > -35 and temperature <= -25:
        temp_coeff = 2.00 
    elif temperature > -25 and temperature <= -15:
        temp_coeff = 1.50
    elif temperature > -15 and temperature <= -5:
        temp_coeff = 1.25
    elif temperature > -5 and temperature <= +5:
        temp_coeff = 1.125
    elif temperature > -15 and temperature <= -10:
        temp_coeff = 1.05

    temp_coeff += abs(temperature-np.round(temperature, 0))

    res = temp_coeff*consumption
    #print(abs(temperature-np.round(temperature, 0)))
    return res

def chargo(charge_rate, temperature):
    temp_coeff = 1.00
    if temperature < -35:
        temp_coeff = 0.20
    elif temperature > -35 and temperature <= -25:
        temp_coeff = 0.50 
    elif temperature > -25 and temperature <= -15:
        temp_coeff = 0.75
    elif temperature > -15 and temperature <= -5:
        temp_coeff = 0.85
    elif temperature > -5 and temperature <= +5:
        temp_coeff = 0.90

    temp_coeff += abs(temperature-np.round(temperature, 0))/100

    res = temp_coeff*charge_rate
    #print(res)
    return res

def cycle_col(col):
    res = col
    if col == 'tab:green':
        res = 'tab:blue'
    elif col == 'tab:blue':
        res = 'tab:cyan'
    elif col == 'tab:cyan':
        res = 'tab:red'
    elif col == 'tab:red':
        res = 'tab:orange'
    elif col == 'tab:orange':
        res = 'tab:olive'
    elif col == 'tab:olive':
        res = 'tab:green'
    return res

## Function modified from one generated by ChatGPT
def expand_array(input_array, length):
    # Get the number of points in the input array
    n = input_array.shape[0]
    # Create an array of indices corresponding to the input points
    indices = np.arange(n)
    # Create an array of indices corresponding to the output points
    new_indices = np.linspace(0, n - 1, length)
    # Interpolate the input data at the output points
    output_array = np.interp(new_indices, indices, input_array)

    return output_array

def scenario_1():
    # DIFFERENT BATTERY TYPES, WITH VARYING CONSUMPTIONS
    battery_1 = Battery('NMC',800, 3.0, 6800)
    battery_2 = Battery('LTO',600, 3.0, 7260)
    machine_1 = Machine('LT15', 7000, battery_1, 100)
    machine_2 = Machine('LT15', 7000, battery_1, 300)
    machine_3 = Machine('LT15', 7000, battery_2, 100)
    machine_4 = Machine('LT15', 7000, battery_2, 300)

    temps_1 = [-19.20, -18.20, -22.01, -19, -20, -21, -20.29, -19.20, -18.10]

    environment = Environment('Skøyen - Spikkestad', 110, [temps_1, temps_1])
    duration = 180


    #######
    info_str_left = ""
    info_str_left += "Stretch:        " + str(environment.name) + "\n" + "Machine:        " + str(machine_1.name) + "\n" + "Battery:        " + str(machine_1.battery.name) + " – " + str(machine_1.battery.capacity) + " kWh\n" + "Consumption (Low):    " + str(machine_1.consumption) + " kWh/h\n" + "Consumption (High):    " + str(machine_2.consumption) + " kWh/h\n"

    info_str_right = ""
    info_str_right += "Stretch:        " + str(environment.name) + "\n" + "Machine:        " + str(machine_3.name) + "\n" + "Battery:        " + str(machine_3.battery.name) + " – " + str(machine_3.battery.capacity) + " kWh\n" + "Consumption (Low):    " + str(machine_3.consumption) + "\n" + "Consumption (High):    " + str(machine_4.consumption) + "\n"


    ax_info_1.text(0, 0, info_str_left, fontsize=12, bbox=props)
    ax_info_2.text(0, 0, info_str_right, fontsize=12, bbox=props)
    #######

    simulato(duration, [machine_1, machine_2, machine_3, machine_4], environment)
    plt.grid()
    plt.show()
    plt.title("Different Consumptions")

def scenario_2():
    # Different Temperatures
    battery_1 = Battery('LTO',600, 1.0, 7260)
    machine_1 = Machine('LT15', 7000, battery_1, 300)

    temps_2 = [-10, -12, -9, -10, -12, -9, -10, -12, -9, -10, -12, -9 ]
    temps_3 = [-10, -40]

    environment = Environment('Skøyen - Spikkestad', 110, [temps_2, temps_3])
    duration = 90

    #######
    info_str_left = ""
    info_str_left += "Stretch:        " + str(environment.name) + "\n" + "Machine:        " + str(machine_1.name) + "\n" + "Battery:        " + str(machine_1.battery.name) + " – " + str(machine_1.battery.capacity) + " kWh\n" + "Consumption (Cold):    " + str(machine_1.consumption) + " kWh/h\n"

    info_str_right = ""
    info_str_right += "Stretch:        " + str(environment.name) + "\n" + "Machine:        " + str(machine_1.name) + "\n" + "Battery:        " + str(machine_1.battery.name) + " – " + str(machine_1.battery.capacity) + " kWh\n" + "Consumption (Colder):    " + str(machine_1.consumption) + " kWh/h\n"


    ax_info_1.text(0, 0, info_str_left, fontsize=12, bbox=props)
    ax_info_2.text(0, 0, info_str_right, fontsize=12, bbox=props)
    #######

    simulato(duration, [machine_1, machine_1], environment)
    plt.grid()
    plt.show()


def scenario_3():
    # Different c_rates
    battery_1 = Battery('LTO',600, 1.0, 7260)
    battery_2 = Battery('LTO',600, 3.0, 7260)
    machine_1 = Machine('LT15', 7000, battery_1, 300)
    machine_2 = Machine('LT15', 7000, battery_2, 300)

    temps_1 = [-19.20, -18.20, -22.01, -19, -20, -21, -20.29, -19.20, -18.10]

    environment = Environment('Skøyen - Spikkestad', 110, [temps_1])
    duration = 180

    simulato(duration, [machine_1, machine_2], environment)

    #######
    info_str_left = ""
    info_str_left += "Stretch:        " + str(environment.name) + "\n" + "Machine:        " + str(machine_1.name) + "\n" + "Battery:        " + str(machine_1.battery.name) + " – " + str(machine_1.battery.capacity) + " kWh\n" + "Consumption:    " + str(machine_1.consumption) + " kWh/h\n" + "C-rate:                " + str(machine_1.battery.charge_rate) + " \n"

    info_str_right = ""
    info_str_right += "Stretch:        " + str(environment.name) + "\n" + "Machine:        " + str(machine_2.name) + "\n" + "Battery:        " + str(machine_2.battery.name) + " – " + str(machine_2.battery.capacity) + " kWh\n" + "Consumption:    " + str(machine_2.consumption) + " kWh/h\n" + "C-rate:                " + str(machine_2.battery.charge_rate) + "\n"


    ax_info_1.text(0, 0, info_str_left, fontsize=12, bbox=props)
    ax_info_2.text(0, 0, info_str_right, fontsize=12, bbox=props)
    #######

    plt.grid()
    plt.show()

def scenario_4():
    # Hydraulic vs Electric consumptions
    battery_1 = Battery('LTO',600, 3.0, 7260)

    machine_1 = Machine('LT15 (Electric)', 7000, battery_1, 177)
    machine_2 = Machine('LT15 ', 7000, battery_1, 295)
    machine_3 = Machine('LT15 (Hydraulic)', 7000, battery_1, 265)
    machine_4 = Machine('LT15', 7000, battery_1, 441)

    temps_1 = [-19.20, -18.20, -22.01, -19, -20, -21, -20.29, -19.20, -18.10]

    environment = Environment('Skøyen - Spikkestad', 110, [temps_1])
    duration = 180

    simulato(duration, [machine_1, machine_2, machine_3, machine_4], environment)

    #######
    info_str_left = ""
    info_str_left += "Stretch:                " + str(environment.name) + "\n" + "Machine:                      " + str(machine_1.name) + "\n" + "Battery:                        " + str(machine_1.battery.name) + " – " + str(machine_1.battery.capacity) + " kWh\n" + "Consumption (Clearing):    " + str(machine_1.consumption) + " kWh/h\n" + "Consumption (Blowing):     " + str(machine_2.consumption) + " kWh/h\n" + "C-rate:                                " + str(machine_1.battery.charge_rate) + "\n"

    info_str_right = ""
    info_str_right += "Stretch:                " + str(environment.name) + "\n" + "Machine:                    " + str(machine_3.name) + "\n" + "Battery:                        " + str(machine_3.battery.name) + " – " + str(machine_3.battery.capacity) + " kWh\n" + "Consumption (Clearing):    " + str(machine_3.consumption) + " kWh/h\n" + "Consumption (Blowing):     " + str(machine_4.consumption) + " kWh/h\n" + "C-rate:                                " + str(machine_3.battery.charge_rate) + "\n"


    ax_info_1.text(0, 0, info_str_left, fontsize=12, bbox=props)
    ax_info_2.text(0, 0, info_str_right, fontsize=12, bbox=props)
    #######

    plt.grid()
    plt.show()

def scenario_5():
    # Diesel v Battery
    # 125.5 MWh
    battery_1 = Battery('LTO', 600, 3.0, 7260)
    battery_2 = Battery('Diesel',33375, 3.0, 1255)

    machine_1 = Machine('LT15', 7000, battery_1, 300)
    machine_2 = Machine('LT15', 7000, battery_2, 300)

    temps_1 = [-19.20, -18.20, -22.01, -19, -20, -21, -20.29, -19.20, -18.10]

    environment = Environment('Skøyen - Spikkestad', 110, [temps_1])
    duration = 600

    simulato(duration, [machine_1, machine_2], environment)

    #######
    info_str_left = ""
    info_str_left += "Stretch:        " + str(environment.name) + "\n" + "Machine:        " + str(machine_2.name) + "\n" + "Diesel equiv.:    " + "12500 L" + " ≃ " + str(machine_2.battery.capacity) + " kWH\n" + "Consumption (Low):    " + str(machine_2.consumption) + " kWh/h\n"

    info_str_right = ""
    info_str_right += "Stretch:        " + str(environment.name) + "\n" + "Machine:        " + str(machine_1.name) + "\n" + "Battery:        " + str(machine_1.battery.name) + " – " + str(machine_1.battery.capacity) + " kWh\n" + "Consumption :    " + str(machine_1.consumption) + "kWh/h\n"


    ax_info_1.text(0, 0, info_str_left, fontsize=12, bbox=props)
    ax_info_2.text(0, 0, info_str_right, fontsize=12, bbox=props)
    #######

    plt.grid()
    plt.show()

scenario_4()