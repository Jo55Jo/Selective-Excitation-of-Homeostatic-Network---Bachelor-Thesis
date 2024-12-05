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
#Runs = [67, 68, 62, 66, 63] # AA plots
Runs = [0.0001, 0.001, 0.01, 0.1, 1]
#Runs = ["/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/AA10000_4_1_RASTER_1101_95.pkl", "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/AA10000_4_0.1_RASTER_1101_95.pkl", "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/AA10000_4_0.01_RASTER_1101_95.pkl", "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/AA10000_4_0.001_RASTER_1101_95.pkl", "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/AA10000_4_0.0001_RASTER_1101_95.pkl"]
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






def Branch_Homeo_Raster(Runs: list):
    total = []
    branching = []
    h_list = []

    num_runs = len(Runs)

    # Subplots erstellen: 3 Zeilen, Anzahl der Runs als Spalten
    fig, axes = plt.subplots(3, num_runs, figsize=(num_runs * 5, 3), dpi=200, squeeze=False)

    for i, run in enumerate(Runs):
        #with open(f"/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/Run_{run}.pkl", 'rb') as file:
        with open(f"/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/AA10000_5_{run}_1501_95.pkl", 'rb') as file:
        #with open(run, 'rb') as file:
            data_dict = pickle.load(file)
            Avalanche_Distribution = data_dict["Avalanche_Distribution"]
            h = data_dict["h"]
            branching_global = data_dict["Branching_global"]
            nn = data_dict["N"]
            Seconds = data_dict["Sec"]
            active_neurons = data_dict["global_act"]

            Total_Activity = np.sum(Avalanche_Distribution)
            Average_Branching = np.average(branching_global[10000:])

            total.append(Total_Activity)
            branching.append(Average_Branching)
            h_list.append(h)
            Average_Activity = data_dict["Average_Activity"]
            Average_Alpha = data_dict["Average_Alpha"]

            # Get color and h-string
            title_h, color = get_h_col(h)

            branching_global = [(x / 4) * 5 for x in branching_global]


            # Branching plot (1. Zeile)
            plot_branching(branching_global[192500:200001], color, title_h, axes[0, i], nn, Seconds)

            # Homeostatic plot (2. Zeile)
            plot_homeostatic(Average_Alpha[67500:75001], color, "h", nn, Seconds, ax=axes[1, i])

            # Raster plot (3. Zeile)
            Raster_plot(active_neurons, color, ax=axes[2, i])

            print("average m_t: ", np.average(branching_global[100000:]))
            print("average alpha: ", np.average(Average_Alpha))

    # Platz anpassen
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, wspace=0.35, hspace=0.7)

    # Gemeinsame Y-Achsenbeschriftungen
    fig.text(0.02, 0.81, 'Average\nBranching\nParameter', 
            va='center', ha='center', rotation='vertical', fontsize=6)
    fig.text(0.02, 0.51, 'Average\nHomeostatic\nParameter', 
            va='center', ha='center', rotation='vertical', fontsize=6)
    fig.text(0.02, 0.21, 'Example\nActivity of 30\nNeurons', 
            va='center', ha='center', rotation='vertical', fontsize=6)


    plt.show()


def plot_homeostatic(homeo_1: list, color_plot: str, h_string: str, N: int, seconds: int, ax=None):
    """
    Plot homeostatic data on a given axis (ax). 
    If no axis is provided, it creates a new plot.

    Parameters:
    - homeo_1 (list): Homeostatic data to plot.
    - color_plot (str): The color of the plot line.
    - h_string (str): The string representation of the parameter h.
    - N (int): The number of neurons (not directly used in this function but might be useful for context).
    - seconds (int): The number of seconds for the x-axis time range.
    - ax (matplotlib axis): The axis to plot on. If None, a new axis will be created.
    """
    # Use the provided axis or create a new one
    if ax is None:
        fig, ax = plt.subplots(figsize=(4, 3), dpi=200)

    # Dynamically calculate font sizes based on subplot size
    title_fontsize = 10
    label_fontsize = 8
    tick_fontsize_y = 6
    tick_fontsize_x = 6

    # X-Axis: Time in discrete time steps (seconds / delta_t)
    x = range(len(homeo_1))
    normalize = 1000 / 4
    y = homeo_1

    # Find the largest and smallest values for the y-axis limits
    max_value = max(homeo_1)
    min_value = min(homeo_1)

    # Customize the axes
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # Set X and Y labels
    #ax.set_xlabel('Seconds', fontsize=label_fontsize, fontweight=500, labelpad=-2)
    ax.set_ylabel(r"$\overline{\alpha}$", fontsize=label_fontsize, fontweight=500, labelpad=20, rotation=0)
    ax.yaxis.set_label_position("left")
    ax.yaxis.set_label_coords(0.01, 1.02)
    ax.set_ylim(min_value - 0.01, max_value + 0.01)

    # Y-ticks at specific values
    y_ticks = [min_value - 0.005, (min_value + max_value) / 2, max_value + 0.005]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f'{tick:.3f}' for tick in y_ticks], fontsize=tick_fontsize_y)

    # Custom x-ticks for the start and end
    x_tick_positions = [0, len(x) - 1]
    x_tick_labels = [int(pos / normalize) for pos in x_tick_positions]
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels(x_tick_labels, fontsize=tick_fontsize_x)

    # Plot the homeostatic data
    ax.plot(x, y, color=color_plot, linewidth=1)

    # Title the subplot
    #ax.set_title(r'$\frac{h}{r^*} = $' + h_string, fontsize=title_fontsize, color=color_plot, pad=10)

    # Optionally, save the plot if needed (not required for subplots)
    output_dir = "Ploting/plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    base_filename = "Homeostatic"
    file_extension = ".png"
    counter = 1
    output_file = os.path.join(output_dir, base_filename + file_extension)
    while os.path.exists(output_file):
        output_file = os.path.join(output_dir, f"{base_filename}_{counter}{file_extension}")
        counter += 1
    # Uncomment to save plot if necessary
    # plt.savefig(output_file)

    # Display the plot (will be handled by plt.show() if needed outside this function)
    # plt.show()

def plot_branching(branch_glob: list, color_plot: str, h_string: str, ax, N: int, seconds: int):
    # X-Achse: Zeit in diskreten Zeitschritten (Sekunden / delta_t)
    x = range(len(branch_glob))
    normalize = 1000 / 4
    y = branch_glob

    # Größter und kleinster Wert aus der Liste
    max_value = max(branch_glob)
    min_value = min(branch_glob)

    # Achsen anpassen
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # X-Achsenbeschriftung
    #ax.set_xlabel('Seconds', fontsize=8, labelpad=-2)

    # Y-Achsenbeschriftung und Begrenzungen
    ax.set_ylabel(r"$m_t$", fontsize=8, labelpad=20, rotation=0)
    ax.yaxis.set_label_position("left")
    ax.yaxis.set_label_coords(0.01, 1.02)
    ax.set_ylim(min_value - 0.01, max_value + 0.01)

    # Y-Achse bei spezifischen Werten beschriften
    y_ticks = [min_value - 0.005, (min_value + max_value) / 2, max_value + 0.005]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f'{tick:.3f}' for tick in y_ticks], fontsize=6)

    # Custom x-ticks für Anfang und Ende
    x_tick_positions = [0, len(x) - 1]
    x_tick_labels = [int(pos / normalize) for pos in x_tick_positions]
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels(x_tick_labels, fontsize=6)

    # Plot the branching activity
    ax.plot(x, y, color=color_plot, linewidth=1)

    # Title (optional, use h_string for labeling)
    ax.set_title(r'$\frac{h}{r^*} = $' + h_string, color=color_plot, fontsize=8, pad=10)

    # Ensure only left and bottom spines are visible
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

def Raster_plot(active_neurons: list, color: str, ax=None):
    """
    Erstellt einen Raster-Plot in einem angegebenen Subplot.

    Parameters:
        active_neurons (list): Liste der aktiven Neuronen zu jedem Zeitpunkt.
        color (str): Farbe der Punkte.
        ax (matplotlib axis): Der Subplot, auf dem der Rasterplot gezeichnet werden soll.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 10), dpi=200)

    # Länge der Daten in Millisekunden
    time_steps = len(active_neurons)

    # Konvertiere die Zeitschritte zu Sekunden
    time_in_seconds = [i / 1000 for i in range(time_steps)]

    # Punkte für das Raster vorbereiten
    x_data = []
    y_data = []

    for t, active in enumerate(active_neurons):
        for neuron in active:
            if 0 <= neuron <= 31:  # Nur Neuronen 0-30 plotten
                x_data.append(time_in_seconds[t])
                y_data.append(neuron)

    # Punkte plotten
    ax.scatter(x_data, y_data, c=color, s=1, alpha=0.8)  # Kleinere Punkte und transparenter
    ax.set_xlabel("Seconds", fontsize=8)
    #ax.set_ylabel("Neuron", fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=6)
    #ax.set_title("Raster Plot", fontsize=8, color=color, pad=10)

    # X-Achse anpassen
    max_seconds = time_steps // 1000
    ax.set_xticks(range(0, max_seconds + 1, 10))  # Ticks alle 10 Sekunden
    ax.set_yticks(range(0, 30+1, 10))  # Ticks alle 10 Sekunden



Branch_Homeo_Raster(Runs)


