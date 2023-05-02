import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import scipy as sp
import matplotlib.gridspec as gridspec



###########################################################
####  PLOT STUFF ####################################### 

gs = gridspec.GridSpec(nrows=3, ncols=2, width_ratios=[1, 1.5], height_ratios=[1, 1, 1.5])

# Create the three axes
fig = plt.figure(constrained_layout=True, figsize=(12, 8))

# Upper GridSpec
gs0 = gridspec.GridSpec(2,1, height_ratios=[2, 1], figure=fig)

# Top Gridspec; Graphs
gs00 = gridspec.GridSpecFromSubplotSpec(ncols=2, nrows=3, width_ratios=[1, 3], height_ratios=[1, 1, 1], subplot_spec=gs0[0])

# Bottom Gridspec: Info
gs01 = gridspec.GridSpecFromSubplotSpec(ncols=4, nrows=1, subplot_spec=gs0[1])

# Define Graph axes
ax0 = fig.add_subplot(gs00[0, 0]) 
ax1 = fig.add_subplot(gs00[1, 0]) 
ax2 = fig.add_subplot(gs00[2, 0]) 
ax3 = fig.add_subplot(gs00[:, 1])

# Define legend axes

textstr = "to"

ax_mach_info = fig.add_subplot(gs01[0,0])
ax_batt_info = fig.add_subplot(gs01[0,1])
ax_envi_info = fig.add_subplot(gs01[0,2])
ax_asso_info = fig.add_subplot(gs01[0,3])

ax_mach_info.axis('off')
ax_batt_info.axis('off')
ax_envi_info.axis('off')
ax_asso_info.axis('off')

props = dict(boxstyle='square', facecolor='white', alpha=0.5)

#fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)

###########################################################
####  FORMULA STUFF ####################################### 

class Environment():
    def __init__(self, name, altitude, temperature):
        self.name = name
        self.altitude = altitude
        self.temperature = temperature

class Machine():
    def __init__(self, name, wattage, weight, Battery):
        self.name = name
        self.wattage = wattage
        self.weight = weight
        self.Battery = Battery
        
class Battery():
    def __init__(self, name, capacity, charge_rate, weight):
        self.name = name
        self.capacity = capacity
        self.charge_rate = charge_rate
        self.weight = weight
        # Temperature dependency

# Nested temperature control should affect the battery
# Perhaps model the box around the battery

def simulate(duration, Machine, Battery, Environment):
    m = Machine
    b = Battery
    e = Environment

    w1 = Machine.wattage    # two consumptions
    w2 = Machine.wattage    #

    t = 0
    temp = Environment.temperature
    alt = Environment.altitude

    time_list, wattage_list_1, wattage_list_2, temp_list, altitude_list, charge_list = [], [], [], [], [], []

    usage_hi = 300/60 #TODO: add these into the Machine object. It's hourly, so /60
    usage_lo = 100/60

    charge=0
    # Running the simulation
    while t<duration:

        temp = temp + np.random.randint(-1,2)
        alt = alt + np.random.randint(-1,2)

        time_list.append(t)
        wattage_list_1.append(w1)
        wattage_list_2.append(w2)
        temp_list.append(temp)
        altitude_list.append(alt)
        charge_list.append(charge)
        t = t+1

        # Making some random temperature & height variations; replace with data
        # TODO: Can also plot altitude and temperatures
        
        temp_coeff = np.abs(1 - temp / 20)
        w1 = w1 - usage_hi * temp_coeff
        #w1 = w1 - battery_depletion(w1,temp,1,0.1)
        
        if(w1<0):
            w1=0
        elif(w1>1000):
            w1=1000

        w2 = w2 - usage_lo * temp_coeff
        #w2 = w2 - battery_depletion(w2,temp,1,0.1)
        
        if(w2<0):
            w2=0
        elif(w2>1000):
            w2=1000


    # Create the plot
    

    # Subgraphs
    ax0.plot(time_list,temp_list, 'tab:orange')
    ax0.set(xlabel='Time [min]', ylabel='Temperature [C]')
    ax1.plot(time_list,altitude_list, 'tab:green')
    ax1.set(xlabel='Time [min]', ylabel='Altitude [m]')
    ax2.plot(time_list,charge_list, 'tab:red')
    ax2.set(xlabel='Time [min]', ylabel='Charging rate')

    # Main Graph
    ax3.plot(time_list,wattage_list_1)
    ax3.plot(time_list,wattage_list_2, 'tab:red')
    ax3.set(xlabel='Time [m]', ylabel='Capacity [kWh]')

    # Info Section
    mach_str = m.name
    batt_str = b.name
    envi_str = e.name
    asso_str = "INFO"

    ax_mach_info.text(
        0.05, 0.95, mach_str, transform=ax_mach_info.transAxes, fontsize=14, va='top', ha='right', bbox=props)
    ax_batt_info.text(
        0.05, 0.95, batt_str, transform=ax_batt_info.transAxes, fontsize=14, va='top', ha='center', bbox=props)
    ax_envi_info.text(
        0.05, 0.95, envi_str, transform=ax_envi_info.transAxes, fontsize=14, va='top', ha='center', bbox=props)
    ax_asso_info.text(
        0.05, 0.95, asso_str, transform=ax_asso_info.transAxes, fontsize=14, va='top', ha='center', bbox=props)



# CHAT GPT
def battery_depletion(capacity, temperature, time, C_rate):
    """
    Simulates battery depletion over time, given a certain capacity, temperature, discharge rate, and time.

    Parameters:
    -----------
    capacity : float
        Battery capacity in watt-hours (Wh)
    temperature : float
        Operational temperature of the battery in degrees Celsius (°C)
    time : array_like
        Discharge time in hours (h)
    C_rate : float
        Discharge rate, expressed as a multiple of the capacity (C)

    Returns:
    --------
    discharge_capacity : array_like
        Discharge capacity over time in ampere-hours (Ah)
    """
    # Convert capacity from Wh to Ah
    voltage = 3.7  # Typical voltage for an NMC battery
    capacity_Ah = capacity / voltage

    # Calculate rate constant k based on temperature
    k_ref = 2.0e-5  # Reference rate constant at 25°C
    E_r = 34500  # Activation energy
    T_ref = 298.15  # Reference temperature in Kelvin
    R = 8.314  # Gas constant
    k = k_ref * np.exp(-E_r / (R * (temperature + 273.15)) + E_r / (R * T_ref))

    # Calculate discharge capacity over time
    discharge_capacity = capacity_Ah * (1 - np.exp(-k * C_rate * time))

    return discharge_capacity


## CHAT-GPT v2
def discharge_capacity(temp, capacity, time):
    # Define the temperature-dependent parameters
    if temp <= 0:
        # Handle the case where the temperature is below 0 degrees Celsius
        C_rate = 0.1
        k = 4.0
    elif temp <= 25:
        # Handle the case where the temperature is between 0 and 25 degrees Celsius
        C_rate = 1.0
        k = 1.0
    elif temp <= 40:
        # Handle the case where the temperature is between 25 and 40 degrees Celsius
        C_rate = 2.0
        k = 0.5
    else:
        # Handle the case where the temperature is above 40 degrees Celsius
        C_rate = 0.5
        k = 2.0
    
    # Calculate the discharge capacity
    discharge_capacity = capacity * np.exp(-k * C_rate * time)
    
    print(discharge_capacity)
    return discharge_capacity


def battery_depletion1(E0, k, t, T, Ea, A):
    """
    Calculates the remaining energy in a battery as a function of time and temperature,
    assuming an exponential decay model with temperature dependence.

    Parameters:
    E0 (float): the initial energy of the battery
    k (float): the decay constant, in units of inverse time
    t (numpy array): an array of time values at which to evaluate the energy
    T (float or numpy array): the temperature of the battery, in Kelvin
    Ea (float): the activation energy, in units of energy per mole
    A (float): the pre-exponential factor, in units of inverse time

    Returns:
    E (numpy array): an array of energy values corresponding to the input time and temperature arrays
    """
    R = 8.314  # gas constant, in units of J/mol/K

    #
    # In this version of the function, we have added three new parameters:

    #T: the temperature of the battery, in Kelvin
    #Ea: the activation energy, which describes the dependence of the decay constant on temperature
    #A: the pre-exponential factor, which is another parameter that describes the temperature dependence of the decay constant.
    #The formula for the remaining energy now includes an additional term that depends on temperature, which is given by A * exp(-Ea/(R*T)), #where R is the gas constant in units of J/mol/K. This term describes the temperature dependence of the decay constant k, and accounts for #the fact that batteries tend to lose energy more quickly at higher temperatures due to increased chemical and electrochemical reactions.

    #Note that the activation energy Ea and pre-exponential factor A are specific to each battery chemistry and geometry, and can be estimated #from experimental data or literature values.

    E = E0 * np.exp(-A * np.exp(-Ea/(R*T)) * t - k * t)
    return E

def deplete(Machine, Environment):
    alt = Environment.alt()
    reduced_w = 50*(alt/100)
    return -reduced_w

## charging function returning the charged wattaged #TODO: Override where you can charge for a set cap, returning time
def charge(current_wattage, time_to_charge, temperature, alt):
    charge_rate = 10*temperature/100
    increased_w = time_to_charge*charge_rate
    return increased_w

def run_1():
    m = Machine('LT15',1000,7000,'NMC')
    b = Battery('NMC', 100,10,500)
    e = Environment('Spikkestad - Skøyen', 110,15)
    duration = 720

    #get_stretch(populate(), duration)

    simulate(duration, m,b,e)
    plt.show()

def run_2():
    m = Machine('LT17',1000,7000,'ABC')
    b = Battery('Diesel', 100,10,500)
    e = Environment('Skøyen - Spikkestad', 110,15)
    duration = 720

    #get_stretch(populate(), duration)

    simulate(duration, m,b,e)
    plt.show()

run_1()