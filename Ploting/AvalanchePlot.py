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

if not smoothed:
    def plot_log_histogram(data, title, col, exponent=-3/2):
        """
        Plots a histogram with logarithmically distributed bins from 10^0 to 10^6 and normalizes the counts to probabilities.
        
        Parameters:
        data (array-like): The data to plot (event sizes).
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
        
        # Erstellen der Figur und Zugriff auf ihre Größe
        fig = plt.figure(figsize=(4,4), dpi=200)
        fig_width, fig_height = fig.get_size_inches()

        # Dynamisch berechnete Schriftgrößen basierend auf der Plotgröße
        title_fontsize = fig_height * 8
        label_fontsize = fig_height * 7
        tick_fontsize_y = fig_height * 5
        tick_fontsize_x = fig_height * 8
        
        # Plot the histogram on a log-log scale
        plt.scatter(bin_centers, probabilities, label='Data', c=col)

        # Set log-log scale
        plt.xscale('log')
        plt.yscale('log')
        
        # Add reference line for s^-2/3
        ref_x = np.logspace(0, 6, num=50)
        ref_y = ref_x ** (-3/2)
        if exponent == -3/2:
            plt.plot(ref_x, ref_y, 'r--', label=r'P(x) = s^{-3/2}$')
        else:
            plt.plot(ref_x, ref_y, 'r--', label=str(exponent))
        
        # Entfernen der Spines, nur links und unten sichtbar
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        plt.gca().spines['left'].set_visible(True)
        plt.gca().spines['bottom'].set_visible(True)

        # Achsenbeschriftungen und Titel
        plt.xlabel('Avalanche Size', fontsize=label_fontsize)
        #plt.ylabel('Avalanche\nDistribution', fontsize=label_fontsize)
        #plt.title(title, fontsize=title_fontsize, color=col)
        plt.legend(fontsize=8)

        # Set custom ticks for x-axis
        plt.xticks([1, 10**2, 10**4, 10**6], [r'$10^0$', r'$10^2$', r'$10^4$', r'$10^6$'], fontsize=tick_fontsize_x)
        plt.yticks(fontsize=tick_fontsize_y)
        
        # Speichern und Anzeigen des Plots
        output_dir = "Ploting/plots"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        base_filename = "Avalanches"
        file_extension = ".png"
        counter = 1
        output_file = os.path.join(output_dir, base_filename + file_extension)
        while os.path.exists(output_file):
            output_file = os.path.join(output_dir, f"{base_filename}_{counter}{file_extension}")
            counter += 1

        # Speichern des Plots
        plt.savefig(output_file)
        plt.show()

if smoothed:
    def moving_average(data, window_size):
        return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

    def plot_log_histogram(data, title, col, exponent=-3/2):
        """
        Plots a smoothed histogram with logarithmically distributed bins and normalizes the counts to probabilities.
        """
        # Define logarithmic bins from 10^0 to 10^6
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
        
        # Apply a moving average to smooth the probabilities
        if len(probabilities) > 1:
            smoothed_probabilities = moving_average(probabilities, window_size=3)
            smoothed_bin_centers = bin_centers[:len(smoothed_probabilities)]  # Bin centers after smoothing
            
            # Erstellen der Figur und Zugriff auf ihre Größe
            fig = plt.figure(figsize=(4, 4), dpi=200)
            fig_width, fig_height = fig.get_size_inches()

            # Dynamisch berechnete Schriftgrößen basierend auf der Plotgröße
            title_fontsize = fig_height * 8
            label_fontsize = fig_height * 7
            tick_fontsize_y = fig_height * 5
            tick_fontsize_x = fig_height * 8
            
            # Plot the smoothed histogram on a log-log scale
            plt.scatter(smoothed_bin_centers, smoothed_probabilities, label='Smoothed Data', c=col)
        else:
            # Erstellen der Figur und Zugriff auf ihre Größe
            fig = plt.figure(figsize=(4, 3), dpi=200)
            fig_width, fig_height = fig.get_size_inches()

            # Dynamisch berechnete Schriftgrößen basierend auf der Plotgröße
            title_fontsize = fig_height * 8
            label_fontsize = fig_height * 7
            tick_fontsize_y = fig_height * 5
            tick_fontsize_x = fig_height * 8
            # Plot original if not enough data for smoothing
            plt.scatter(bin_centers, probabilities, label='Data', c=col)
        
        # Set log-log scale
        plt.xscale('log')
        plt.yscale('log')
        
        # Add reference line for s^-2/3
        ref_x = np.logspace(0, 6, num=50)
        ref_y = ref_x ** (exponent)
        if exponent == -3/2:
            plt.plot(ref_x, ref_y, 'r--', label=r'$P(s) = s^{-3/2}$')
        else:
            plt.plot(ref_x, ref_y, 'r--', label=str(exponent))

        # Entfernen der Spines, nur links und unten sichtbar
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        plt.gca().spines['left'].set_visible(True)
        plt.gca().spines['bottom'].set_visible(True)

        # Achsenbeschriftungen und Titel
        plt.xlabel('Avalanche Size', fontsize=label_fontsize)
        #plt.ylabel('Avalanche\nDistribution', fontsize=label_fontsize)
        #plt.title(title, fontsize=title_fontsize, color=col, pad = 35)
        plt.legend(fontsize=8)

        # Set custom ticks for x-axis
        plt.xticks([1, 10**2, 10**4, 10**6], [r'$10^0$', r'$10^2$', r'$10^4$', r'$10^6$'], fontsize=tick_fontsize_x)
        plt.yticks(fontsize=tick_fontsize_y)
        
        # Speichern und Anzeigen des Plots
        output_dir = "Ploting/plots"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        base_filename = "Avalanches"
        file_extension = ".png"
        counter = 1
        output_file = os.path.join(output_dir, base_filename + file_extension)
        while os.path.exists(output_file):
            output_file = os.path.join(output_dir, f"{base_filename}_{counter}{file_extension}")
            counter += 1

        # Speichern des Plots
        plt.savefig(output_file)
        plt.show()

