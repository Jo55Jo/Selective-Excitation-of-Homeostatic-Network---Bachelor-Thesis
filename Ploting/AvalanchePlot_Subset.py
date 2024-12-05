import matplotlib.pyplot as plt 
import numpy as np
from Functions_Constants_Meters import Constants as cons
import os

# Subplot-Konfigurationseinstellungen
plt.rcParams['figure.subplot.left'] = 0.2
plt.rcParams['figure.subplot.right'] = 0.9
plt.rcParams['figure.subplot.bottom'] = 0.3
plt.rcParams['figure.subplot.top'] = 0.9
plt.rcParams['figure.subplot.wspace'] = 0.2
plt.rcParams['figure.subplot.hspace'] = 0.2

smoothed = True

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def plot_log_histogram(data_sub, data_rest, title, col_sub, col_rest, smoothed):
    # Define logarithmic bins from 10^0 to 10^6
    bin_edges = np.logspace(0, 6, num=50)

    fig, ax = plt.subplots(figsize=(4, 3), dpi=200)
    fig_width, fig_height = fig.get_size_inches()

    # Dynamisch berechnete Schriftgrößen basierend auf der Plotgröße
    title_fontsize = fig_height * 8
    label_fontsize = fig_height * 7
    tick_fontsize_y = fig_height * 5
    tick_fontsize_x = fig_height * 8
    
    # Helper function to compute histogram and plot data
    def plot_data(data, label, color, bin_edges):
        counts, _ = np.histogram(data, bins=bin_edges)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_widths = bin_edges[1:] - bin_edges[:-1]
        probabilities = counts / (counts.sum() * bin_widths)
        
        non_zero = counts > 0
        bin_centers = bin_centers[non_zero]
        probabilities = probabilities[non_zero]
        
        if smoothed and len(probabilities) > 1:
            smoothed_probabilities = moving_average(probabilities, window_size=3)
            smoothed_bin_centers = bin_centers[:len(smoothed_probabilities)]
            ax.scatter(smoothed_bin_centers, smoothed_probabilities, label=f'Smoothed {label}', color=color)
        else:
            ax.scatter(bin_centers, probabilities, label=label, color=color)
    
    # Plot data for sub and rest datasets
    plot_data(data_sub, label='Sub', color=col_sub, bin_edges=bin_edges)
    plot_data(data_rest, label='Rest', color=col_rest, bin_edges=bin_edges)
    
    # Set log-log scale
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    # Add reference line for s^-3/2
    ref_x = np.logspace(0, 6, num=50)
    ref_y = ref_x ** (-3/2)
    ax.plot(ref_x, ref_y, 'r--', label=r'$P(s) = s^{-3/2}$')
    
    # Hide all spines, then make only the left and bottom axes visible
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    
    # Labels and title
    ax.set_xlabel('Avalanche Size', fontsize=label_fontsize)
    #ax.set_ylabel('Avalanche\nDistribution', fontsize=label_fontsize)
    #ax.set_title(title, color=col_sub, fontsize=title_fontsize, pad = 25)
    ax.legend(fontsize=8)

    # Customizing tick fonts
    plt.xticks([10**i for i in [0, 2, 4, 6]], fontsize=tick_fontsize_x)  # Set specific x-ticks
    plt.yticks(fontsize=tick_fontsize_y)

    # Save the plot in the plots directory
    output_dir = "Ploting/plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Filename with counter for history
    base_filename = "Avalanche_Distribution_sub"
    file_extension = ".png"
    counter = 1
    output_file = os.path.join(output_dir, base_filename + file_extension)
    while os.path.exists(output_file):
        output_file = os.path.join(output_dir, f"{base_filename}_{counter}{file_extension}")
        counter += 1
    
    # Save the plot
    plt.savefig(output_file)
    plt.show()
