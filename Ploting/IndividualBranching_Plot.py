import matplotlib.pyplot as plt
import numpy as np

def Individual_m(indi: list, h_string: str, color: str):
    # Get the dimensions of the data
    num_time_steps = len(indi)  # Total number of lists (time steps)
    num_nodes = len(indi[0])  # Number of branching parameters per list

    # Convert the list of lists to a 2D numpy array for easier flattening
    data = np.array(indi)

    # Initialize the figure and 3D axis
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Define the x, y, and z positions for each bar
    x = np.arange(num_nodes)
    y = np.arange(0, num_time_steps * 0.1, 0.1)  # each list represents 0.1s
    x, y = np.meshgrid(x, y)

    # Flatten the arrays to create a single bar for each combination of (node, time)
    x = x.flatten()
    y = y.flatten()
    z = np.zeros_like(x)

    # Flatten the data for z-axis values (branching parameters) and set the bar height
    dx = dy = 0.8  # width of the bars in x and y
    dz = data.flatten()  # heights corresponding to branching parameter values

    # Plot the 3D bar plot
    ax.bar3d(x, y, z, dx, dy, dz, color=color, shade=True)

    # Set axis labels and title
    ax.set_xlabel('Node (Branching Parameter)')
    ax.set_ylabel('Time (s)')
    ax.set_zlabel('Branching Parameter Strength')
    ax.set_title(f'Branching Parameter Distribution - {h_string}')

    # Customizing y-axis ticks to display every 10 seconds (or 100 steps of 0.1s each)
    ax.set_yticks(np.arange(0, num_time_steps * 0.1, 10))  # change 10 to tick interval as needed

    # Show the plot
    plt.show()


def Individual_2D(data: list, h_string: str, color: str):
    """
    Create a 2D bar plot for branching parameter values.

    Parameters:
    - data (list): A single list representing branching parameter values for nodes.
    - h_string (str): A title string for the plot.
    - color (str): Color for the bars.
    """
    # Convert the input list to a numpy array
    data = np.array(data)

    # Generate the x-axis values (Node indices)
    x = np.arange(len(data))

    # Create the bar plot
    plt.figure(figsize=(10, 7))
    plt.bar(x, data, color=color, alpha=0.8)

    # Set axis labels and title
    plt.xlabel('Node (Branching Parameter)')
    plt.ylabel('Branching Parameter Strength')
    plt.title(f'Branching Parameter Distribution - {h_string}')

    # Show the plot
    plt.show()


