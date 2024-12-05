import pickle
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pickle

import os
# append parent directory for importing constants
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
from Functions_Constants_Meters import Constants as cons

# First define whether it is an subset run or not and whether it is a new one with time etc
plot = True
cons.Subset = False
time = False
is_ER_Run = False
BranchIndi = True
# plot spiking distribution, Runs gibt die Nummern der Runs an, fals subset wird automatisch auf subset gewchselt in dem pfad
spiking_distribution = False
#Runs = [i for i in range(61,68)]
Runs = [67, 68, 62, 66, 63] # AA plots
#Runs = [f"/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/22.11._homogenous/SC_Compiled10000_10_0.1_1301_95.pkl", f"/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/22.11._homogenous/SC_Compiled10000_10_0.03162277660168379_1301_95.pkl", f"/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/22.11._homogenous/SC_Compiled10000_10_0.01_1301_95.pkl"]
# Runs = [75, 74, 73, 72] # AA 
#Runs  = [93, 92, 91, 86, 90 ,83 ,82 , 84, 85] # SC Sub
Runs.reverse()
# Sec = 0 means the whole data  is plottet, Sec ≠ 0 means 30 secs from that point on 
Sec = 30


def get_h_col(h):
     # getting the title h and the plotting color 
    if h == 10:
        title_h = r'$10^1$'
        color = '#FF1493'
    if h == 1:
        title_h = r'$10^0$'
        color = "green"
    elif h == 10**(-0.75):
        title_h = r'$10^{-0.75}$'
        color = "#FFFF00"
    elif h == 0.1:
        title_h = r'$10^{-1}$'
        color = "#FFD720"
    elif h == 10**(-1.25):
        title_h = r'$10^{-1.25}$'
        color = "#FFC000" 
    elif h == 10**(-1.5):
        title_h = r'$10^{-1.5}$'
        color = "#FFAA00"
    elif h == 10**(-1.75):
        title_h = r'$10^{-1.75}$'
        color = "#FF9500" 
    elif h == 10**(-2):
        title_h = r'$10^{-2}$'
        color = "#FF8000"
    elif h == 10**(-2.25):
        title_h = r'$10^{-2.25}$'
        color = "#FF6A00"
    elif h == 10**(-2.5):
        title_h = r'$10^{-2.5}$'
        color = "#FF5500"
    elif h == 0.001:
        title_h = r'$10^{-3}$'
        color = "#BF0404"
    elif h == 0.0001:
        title_h = r'$10^{-4}$'
        color = "#8404D9"
    elif h == 0.00001:
        title_h = r'$10^{-5}$'
        color = "blue"
    else:
        title_h = r'$10^{-6}$'
        color = "brown"
    return title_h, color






def AA_Plot(Runs: list):
    total = []
    branching = []
    h_list = []
    
    num_runs = len(Runs)
    
    # Subplots erstellen: 2 Zeilen, Anzahl der Runs als Spalten
    fig, axes = plt.subplots(2, num_runs, figsize=(num_runs * 5, 3), dpi=200, squeeze=False)
    

    for i, run in enumerate(Runs):
        with open(f"/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/Run_{run}.pkl", 'rb') as file:
        #with open(run, 'rb') as file:
            data_dict = pickle.load(file)
            Avalanche_Distribution = data_dict["Avalanche_Distribution"]
            h = data_dict["h"]
            branching_global = data_dict["Branching_global"]

            Total_Activity = np.sum(Avalanche_Distribution)
            Average_Branching = np.average(branching_global[10000:])
            
            total.append(Total_Activity)
            branching.append(Average_Branching)
            h_list.append(h)
            Average_Activity = data_dict["Average_Activity"]
            
            # get color and h-string
            title_h, color = get_h_col(h)
            
            # Activity plot in der ersten Zeile
            create_activityplot_subplot(Average_Activity, color, title_h, axes[0, i], Sec, duration=30)
            
            # Avalanche plot in der zweiten Zeile
            avalanche_plot(Avalanche_Distribution, f"Avalanche {run}", color, ax=axes[1, i])

    # Platz anpassen: mehr Abstand links
    plt.tight_layout()
    plt.subplots_adjust(left=0.12, wspace=0.4, hspace=0.55)  # `left` erhöht Abstand links

    # Gemeinsame Y-Achsenbeschriftungen hinzufügen
    #fig.text(0.02, 0.75, 'spiking activity (Hz)', va='center', rotation='vertical', fontsize=8)
    #fig.text(0.02, 0.25, 'avalanche size\n  distribution', va='center', rotation='vertical', fontsize=8)
    fig.text(0.02, 0.75, '    spiking\n activity (Hz)', va='center', rotation='vertical', fontsize=8)
    fig.text(0.02, 0.25, 'avalanche size\n  distribution', va='center', rotation='vertical', fontsize=8)
    plt.show()


def moving_average(data, window_size):

    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def avalanche_plot(data, title, col, ax, exponent=-3/2, smoothed=True, window_size=3):
    """
    Plots a histogram with logarithmically distributed bins from 10^0 to 10^6 and normalizes the counts to probabilities.
    Optionally smooths the histogram data using a moving average.
    
    Parameters:
    data (array-like): The data to plot (event sizes).
    ax: Matplotlib axis to draw the plot on.
    smoothed (bool): Whether to apply smoothing to the data.
    window_size (int): The window size for the moving average if smoothing is enabled.
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
    
    # Apply smoothing if enabled
    if smoothed:
        probabilities = moving_average(probabilities, window_size)
        bin_centers = bin_centers[:len(probabilities)]  # Adjust bin centers after smoothing
    
    # Plot the histogram on a log-log scale
    ax.scatter(bin_centers, probabilities, label='Data', c=col, s=10)

    # Set log-log scale
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    # Add reference line for s^-exponent
    ref_x = np.logspace(0, 6, num=50)
    ref_y = ref_x ** exponent
    ax.plot(ref_x, ref_y, 'r--', label=r'$s^{-3/2}$')
    
    # Formatting
    ax.set_xlabel('avalanche size s', fontsize=8, labelpad=10)
    ax.legend(fontsize=5, frameon=False, bbox_to_anchor=(0.9, 1))

    # Customize ticks
    ax.set_xticks([1, 10**2, 10**4, 10**6])
    ax.set_xticklabels([r'$10^0$', r'$10^2$', r'$10^4$', r'$10^6$'], fontsize=6)
    ax.tick_params(axis='y', which='both', labelsize=6)

    # Only left and bottom spines visible
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)



def create_activityplot_subplot(activity_list: list, color_plot: str, h_string: str, ax, Sec: int = 0, duration: int = 30):
    # Normalize: Zeitschritte pro Sekunde
    time_steps_per_second = 1000 / 4  # Anzahl der Zeitschritte pro Sekunde
    
    if Sec > 0:
        # Start- und End-Index basierend auf den Sekunden
        start_index = int(Sec * time_steps_per_second)
        end_index = int((Sec + duration) * time_steps_per_second)

        # Sicherstellen, dass die Indizes im gültigen Bereich liegen
        start_index = max(0, start_index)
        end_index = min(len(activity_list), end_index)

        # Passenden Bereich auswählen
        x = range(end_index - start_index)
        y = activity_list[start_index:end_index]
    else:
        # Gesamte Liste verwenden
        x = range(len(activity_list))
        y = activity_list

    # Zeitpunkte in Sekunden berechnen
    seconds = [i / time_steps_per_second for i in x]

    # Plotten auf der Achse ax
    ax.plot(seconds, y, color=color_plot, linewidth=1)

    # X-Achsen-Beschriftungen: nur alle 10 Sekunden
    max_seconds = max(seconds)
    x_tick_positions = list(range(0, int(max_seconds) + 2, 10))  # Alle 10 Sekunden
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels(x_tick_positions, fontsize=6)

    # Y-Achsenlimits und Labels
    ax.set_ylim(0, 40)
    ax.set_yticks([0, 20])
    ax.set_ylabel(r'$a_t$ (Hz)', fontsize=8, labelpad=20, rotation=0)
    ax.yaxis.set_label_position("left")
    ax.yaxis.set_label_coords(-0.1, 1.0)
    ax.set_xlabel('seconds', fontsize=8)

    # Titel
    if not cons.log_r:
        ax.set_title(r'$\frac{h}{r^*} = $' + h_string, color=color_plot, fontsize=8, pad=10)
    else:
        ax.set_title(r'$\frac{h}{r^*} = $' + h_string + " log_r", color=color_plot, fontsize=8, pad=10)

    # Nur linke und untere Achsenlinien anzeigen
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)







AA_Plot(Runs)