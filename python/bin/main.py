import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


####
#fig, ax = plt.subplots()
#t = np.linspace(0, 120, 120)
#g = -9.81
#v0 = 12
#v02 = 5


plot_a, plot_b = plt.subplot()

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('A single plot')


# DIMENSIONS FOR THE VEHICLE


#formula1 = g * t**2 / 2 + v0 * t
#formula2 = start_Cap - t


#scat = ax.scatter(t[0], formula1[0], c="b", s=5, label=f'v0 = {v0} m/s')
#line2 = ax.plot(t[0], formula2[0], label=f'v0 = {v02} m/s')[0]
#ax.set(xlabel='Time [m]', ylabel='Capacity [kWh]')
#ax.legend()

###########################################################
####  FORMULA STUFF ####################################### 


start_Cap = 1000 
own_weight = 7000

start_time = 0
start_wattage = 1000 

start_temperature = 15
start_altitude = 110

x = []
y = []

def calculate():

    w = start_wattage
    t = start_time
    temp = start_temperature
    alt = start_altitude

    while w > 0:
        if t > 2000:
            break

        x.append(t)
        t = t+1

        # Making some random temperature & height variations; replace with data
        # TODO: Can also plot altitude and temperatures
        
        temp = temp + np.random.randint(-1,1)
        alt = alt + np.random.randint(-1,1)

        w = deplete(w, t, temp, alt)
        try:
            w =charge(w, t)
        except:
            pass
        y.append(w)


    # Create the plot
    plot_a.plot(x,y)


def deplete(w, t, temp, alt):
    reduced_w = w - t*100
    return reduced_w

def charge(w,t):
    if t % 1235 == 0:
        return w+200
    else:
        return w

###########################################################
####  RENDERING STUFF ####################################### 

#def update(frame):
    # for each frame, update the data stored on each artist.
    #x = t[:frame]
    #y = formula2[:frame]
    # update the scatter plot:
   # data = np.stack([x, y]).T
    #scat.set_offsets(data)
    # update the line plot:
  #  line2.set_xdata(t[:frame])
 #   line2.set_ydata(formula2[:frame])
#    return (line2)




def run():
    #ani = animation.FuncAnimation(fig=fig, func=update, frames=40, interval=30)

    calculate()
    plt.show()

run()