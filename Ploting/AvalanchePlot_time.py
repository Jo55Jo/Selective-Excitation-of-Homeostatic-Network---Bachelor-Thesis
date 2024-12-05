import matplotlib.pyplot as plt 
import numpy as np
from Functions_Constants_Meters import Constants as cons
import os

# Subplot-Konfigurationseinstellungen
plt.rcParams['figure.subplot.left'] = 0.1
plt.rcParams['figure.subplot.right'] = 0.9
plt.rcParams['figure.subplot.bottom'] = 0.2
plt.rcParams['figure.subplot.top'] = 0.7
plt.rcParams['figure.subplot.wspace'] = 0.2
plt.rcParams['figure.subplot.hspace'] = 0.2

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def plot_log_histogram(data, title, col, smoothed):
    """
    Plots a histogram with logarithmically distributed bins from 10^0 to 10^6,
    normalizes the counts to probabilities, and optionally applies smoothing.
    
    Parameters:
    data (array-like): The data to plot (event sizes).
    title (str): Title of the plot.
    col (str): Color for the plot.
    smoothed (bool): Whether to apply smoothing with a moving average.
    """
    # Define logarithmic bins from 10^0 to 10^6
    bin_edges = np.logspace(0, 6, num=50)
    
    # Compute the histogram
    counts, bin_edges = np.histogram(data, bins=bin_edges)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Calculate the probabilities
    bin_widths = bin_edges[1:] - bin_edges[:-1]
    probabilities = counts / (counts.sum() * bin_widths)
    
    # Filter non-zero bins
    non_zero = counts > 0
    bin_centers = bin_centers[non_zero]
    probabilities = probabilities[non_zero]
    
    # Apply smoothing if requested and there’s enough data
    plt.figure(figsize=(6, 4))


    if smoothed and len(probabilities) > 1:
        smoothed_probabilities = moving_average(probabilities, window_size=3)
        smoothed_bin_centers = bin_centers[:len(smoothed_probabilities)]
        plt.scatter(smoothed_bin_centers, smoothed_probabilities, label='Smoothed Data', color=col)
    else:
        plt.scatter(bin_centers, probabilities, label='Data', color=col)
    
    # Set log-log scale
    plt.xscale('log')
    plt.yscale('log')
    
    # Add reference line for s^-2
    ref_x = np.logspace(0, 6, num=50)
    ref_y = ref_x ** (-2)
    plt.plot(ref_x, ref_y, 'r--', label=r'Reference line $s^{-2}$')
    
    # Adjust axes visibility
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.gca().spines['left'].set_visible(True)
    plt.gca().spines['bottom'].set_visible(True)
    
    # Labels and title
    plt.xlabel('Avalanche Size', fontsize=16)
    plt.ylabel('Probability', fontsize=16)
    plt.title(title, fontsize=20, color=col)
    plt.legend()

    # Save the plot in the plots directory
    output_dir = "Ploting/plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Base filename without extension
    base_filename = "Avalanches"
    file_extension = ".png"

    # Find a non-existent filename by appending a number
    counter = 1
    output_file = os.path.join(output_dir, base_filename + file_extension)
    while os.path.exists(output_file):
        output_file = os.path.join(output_dir, f"{base_filename}_{counter}{file_extension}")
        counter += 1

    # Save the plot
    plt.savefig(output_file)
    plt.show()
