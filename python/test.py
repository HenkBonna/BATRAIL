import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def two_plus_one():
    # Create a GridSpec with 2 rows and 2 columns
    gs = GridSpec(nrows=2, ncols=2, width_ratios=[1, 1.5])

    # Create the three axes
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[:, 1])

    # Add some content to the axes for demonstration purposes
    ax1.plot([1, 2, 3], [4, 5, 6])
    ax2.plot([3, 2, 1], [6, 5, 4])
    ax3.plot([1, 2, 3], [6, 5, 4])

    # Add some labels to the axes
    ax1.set_title('Plot 1')
    ax2.set_title('Plot 2')
    ax3.set_title('Plot 3')

    # Adjust the spacing between the subplots
    fig.subplots_adjust(wspace=0.3, hspace=0.3)

    # Show the plot
    plt.show()


def three_plus_two():
    # Create a GridSpec with 3 rows and 2 columns
    gs = GridSpec(nrows=3, ncols=2, width_ratios=[1, 1.5], height_ratios=[1, 1, 1.5])

    # Create the three axes
    fig = plt.figure(figsize=(10, 8))
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[2, 0])
    ax4 = fig.add_subplot(gs[:2, 1])
    ax5 = fig.add_subplot(gs[2, 1])

    # Add some content to the axes for demonstration purposes
    ax1.plot([1, 2, 3], [4, 5, 6])
    ax2.plot([3, 2, 1], [6, 5, 4])
    ax3.plot([2, 4, 6], [8, 7, 5])
    ax4.plot([1, 2, 3], [4, 5, 6])
    ax5.plot([3, 2, 1], [6, 5, 4])

    # Add some labels to the axes
    ax1.set_title('Plot 1')
    ax2.set_title('Plot 2')
    ax3.set_title('Plot 3')
    ax4.set_title('Plot 4')
    ax5.set_title('Plot 5')

    # Adjust the spacing between the subplots
    fig.subplots_adjust(wspace=0.3, hspace=0.3)

    # Show the plot
    plt.show()

def three_plus_one():
    # Define data for the plots
    x = [1, 2, 3, 4, 5]
    y1 = [1, 4, 9, 16, 25]
    y2 = [1, 2, 4, 8, 16]
    y3 = [1, 3, 6, 10, 15]
    y4 = [5, 10, 15, 20, 25]

    # Create the figure and axes using subplot_mosaic
    fig = plt.figure(constrained_layout=True)
    spec = fig.add_gridspec(ncols=2, nrows=3, width_ratios=[1, 2], height_ratios=[1, 1, 1])
    axs = [fig.add_subplot(spec[0, 0]), fig.add_subplot(spec[1, 0]), fig.add_subplot(spec[2, 0]), fig.add_subplot(spec[:, 1])]

    # Plot the data on the axes
    axs[0].plot(x, y1)
    axs[1].plot(x, y2)
    axs[2].plot(x, y3)
    axs[3].plot(x, y4)

    # Add labels to the axes
    axs[0].set_xlabel('x')
    axs[0].set_ylabel('y1')
    axs[1].set_xlabel('x')
    axs[1].set_ylabel('y2')
    axs[2].set_xlabel('x')
    axs[2].set_ylabel('y3')
    axs[3].set_xlabel('x')
    axs[3].set_ylabel('y4')

    # Add a title to the figure
    fig.suptitle('Three Axes to the Left and One Large Axis to the Right')

    # Display the figure
    plt.show()

