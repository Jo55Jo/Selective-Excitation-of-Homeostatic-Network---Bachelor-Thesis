import matplotlib.pyplot as plt
import numpy as np

# Subplot configuration settings
plt.rcParams['figure.subplot.left'] = 0.15
plt.rcParams['figure.subplot.right'] = 0.9
plt.rcParams['figure.subplot.bottom'] = 0.2
plt.rcParams['figure.subplot.top'] = 0.9
plt.rcParams['figure.subplot.wspace'] = 0.2
plt.rcParams['figure.subplot.hspace'] = 0.2

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def plot_spike_dist(data, titles, colors, smoothed=True):
    """
    Plots multiple histograms with logarithmically distributed bins, normalizing the counts to probabilities.
    Each dataset is plotted with its own color and title.

    Parameters:
    data (list of lists): A list of datasets to plot (event sizes for each).
    titles (list of str): Titles for each dataset.
    colors (list of str): Colors for each dataset.
    smoothed (bool): If True, applies a moving average to smooth the probabilities.
    """
    # Define logarithmic bins from 10^-1 to 10^3
    bin_edges = np.logspace(-1, 3, num=50)
    
    # Create figure and set dynamic font sizes based on plot size
    fig = plt.figure(figsize=(4, 4), dpi=200)
    fig_width, fig_height = fig.get_size_inches()
    title_fontsize = fig_height * 8
    label_fontsize = fig_height * 4
    tick_fontsize_y = fig_height * 3.5
    tick_fontsize_x = fig_height * 3
    
    # Iterate through each dataset and plot
    for idx, dataset in enumerate(data):
        counts, _ = np.histogram(dataset, bins=bin_edges)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        # Calculate the probabilities
        bin_widths = bin_edges[1:] - bin_edges[:-1]
        probabilities = counts / (counts.sum() * bin_widths)

        # Filter non-zero bins
        non_zero = counts > 0
        bin_centers = bin_centers[non_zero]
        probabilities = probabilities[non_zero]
        
        # Apply smoothing if requested
        if smoothed and len(probabilities) > 1:
            probabilities = moving_average(probabilities, window_size=3)
            bin_centers = bin_centers[:len(probabilities)]
        
        # Plot histogram on a log-log scale
        plt.scatter(bin_centers, probabilities, label=titles[idx], c=colors[idx])

    # Set log-log scale
    plt.xscale('log')
    plt.yscale('log')
    
    # Configure axes and legend
    plt.xlabel(r'spiking activity $a_t$ (Hz)', fontsize=label_fontsize)
    plt.legend(fontsize=8)

    # Entfernen der Spines, nur links und unten sichtbar
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.gca().spines['left'].set_visible(True)
    plt.gca().spines['bottom'].set_visible(True)

    # Set custom ticks for x-axis, adjusting for the new range
    plt.xticks([10**-1, 10**0, 10**1, 10**2, 10**3], [r'$10^{-1}$', r'$10^0$', r'$10^1$', r'$10^2$', r'$10^3$'], fontsize=tick_fontsize_x)
    plt.yticks(fontsize=tick_fontsize_y)
    
    plt.show()


