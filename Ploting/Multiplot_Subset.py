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
cons.Subset = True
time = False
is_ER_Run = False
BranchIndi = False
spiking_distribution = False

Sec = 710


SC_Subset_Random_GRIFFITH = [
    "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/THESIS_RUNS/SC_Compiled10000_15_0.1_1501_500_99.pkl",
    "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/THESIS_RUNS/SC_Compiled10000_15_0.05623413251903491_1501_500_99.pkl",
    "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/THESIS_RUNS/SC_Compiled10000_15_0.03162277660168379_1501_500_99.pkl",
    "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/THESIS_RUNS/SC_Compiled10000_15_0.01778279410038923_1501_500_99.pkl",
    "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/THESIS_RUNS/SC_Compiled10000_15_0.01_1501_500_99.pkl", 
    "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/THESIS_RUNS/SC_Compiled10000_15_0.005623413251903491_1501_500_99.pkl",
    "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/THESIS_RUNS/SC_Compiled10000_15_0.0031622776601683794_1501_500_99.pkl"
]
SC_Subset_Random_Classic = [
    "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/THESIS_RUNS/SC_Compiled10000_15_0.1_1501_500_99.pkl",
    "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/THESIS_RUNS/SC_Compiled10000_15_0.01_1501_500_99.pkl",
    "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/THESIS_RUNS/SC_Compiled10000_15_0.001_1501_500_99.pkl",
    "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/THESIS_RUNS/SC_Compiled10000_15_0.0001_1501_500_99.pkl"
]


title = "Spacial Clustered - Random Subset"



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
    elif h == 10**(-2.75):
        title_h = r'$10^{-2.75}$'
        color = "#FF3500"
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






def AA_Plot(Runs: list, homogenous=False):
    total = []
    branching = []
    h_list = []
    H_LIST = []
    AVA_DIST_LIST = []
    COLOR_LIST = []
    
    num_runs = len(Runs)
    
    # Subplots erstellen: 2 Zeilen, Anzahl der Runs als Spalten
    fig, axes = plt.subplots(3, num_runs, figsize=(num_runs * 5, 4.1), dpi=200, squeeze=False)
    fig.suptitle("Spacial Clustered - Subset500", fontsize=16, y=0.95) 
    
    #for i, run in enumerate(Runs):
    #    with open(f"/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit/Runtime_Data/Run_{run}.pkl", 'rb') as file:
    for i, run in enumerate(Runs):
        with open(run, 'rb') as file:
            data_dict = pickle.load(file)
        if not homogenous:
            Avalanche_Distribution = data_dict["Avalanche_Distribution"]
            print("Avalanche Distribution: ", i, len(Avalanche_Distribution))
            if i == 0:
                print("External Input = 1: ", Avalanche_Distribution)
            h = data_dict["h"]
            branching_global = data_dict["Branching_global"]

            Total_Activity = np.sum(Avalanche_Distribution)
            Average_Branching = np.average(branching_global[10000:])
            
            total.append(Total_Activity)
            branching.append(Average_Branching)
            h_list.append(h)

            # get color and h-string
            title_h, color = get_h_col(h)

            H_LIST.append(title_h)
            COLOR_LIST.append(color)
            AVA_DIST_LIST.append(Avalanche_Distribution)
            
        if homogenous:
            h = data_dict["h"]
            Avalanche_Distribution = data_dict["Avalanche_Distribution"]
            Average_Activity = data_dict["Average_Activity"]
            title_h, color = get_h_col(h)

            H_LIST.append(title_h)
            COLOR_LIST.append(color)
            AVA_DIST_LIST.append(Avalanche_Distribution)




    return AVA_DIST_LIST, H_LIST, COLOR_LIST

def Spiking_Plot(Runs: list, homogenous=False):

    title_list = [
    "Spacial Clustered\nSubset Centered", 
    "Spacial Clustered\nSubset Random",
    "Erdos Renyi\nSubset",
    "Spacial Clustered\nHomogenous"
    ]

    total = []
    branching = []
    h_list = []
    H_LIST = []
    AVA_DIST_LIST = []
    COLOR_LIST = []

    Sec=200
    
    num_runs = len(Runs[0])  # Anzahl der Runs innerhalb einer Liste
    num_rows = len(Runs)  # Anzahl der Reihen (entspricht der Anzahl der Listen)
    
    # Subplots erstellen: 4 Zeilen, Anzahl der Runs als Spalten
    fig, axes = plt.subplots(num_rows, num_runs, figsize=(num_runs * 2, num_rows*1.5), dpi=200, squeeze=False)

    
    for row_idx, run_list in enumerate(Runs):  # Über die Listen iterieren
        print(row_idx)
        for col_idx, run in enumerate(run_list):  # Über die Dateien in der Liste iterieren
            with open(run, 'rb') as file:
                data_dict = pickle.load(file)
            if row_idx == 3:
                h = data_dict["h"]
                Average_Activity = data_dict["Average_Activity"]
                
                # get color and h-string
                title_h, color = get_h_col(h)


                # Spiking-Aktivität plotten
                if col_idx==2:
                    create_activityplot_homogenous(
                        Average_Activity, color,
                        title_h, ax=axes[row_idx, col_idx], Seconds=200, duration=30, ext_title=False, legend=False, x_title=True
                    )
                elif col_idx==0:
                    create_activityplot_homogenous(
                        Average_Activity, color,
                        title_h, ax=axes[row_idx, col_idx], Seconds=200, duration=30, ext_title=False, legend=False, x_title=False, y_title=title_list[row_idx]
                    )

                else:
                    create_activityplot_homogenous(
                        Average_Activity, color,
                        title_h, ax=axes[row_idx, col_idx], Seconds=200, duration=30, ext_title=False, legend=False, x_title=False
                    )
            #create_activityplot_homogenous(activity_list1: list, color_plot1: str, h_string: str, ax, Seconds: int = 0, duration: int = 30):
            else:
                h = data_dict["h"]
                Average_Activity_rest = data_dict["Average_Activity_rest"]
                Average_Activity_sub = data_dict["Average_Activity_sub"]
                
                # get color and h-string
                title_h, color = get_h_col(h)
                H_LIST.append(title_h)
                COLOR_LIST.append(color)

                # Spiking-Aktivität plotten
                if row_idx == 0 and col_idx == 0:
                    create_activityplot_subset_subplot(
                        Average_Activity_sub, Average_Activity_rest, color, "blue", 
                        title_h, ax=axes[row_idx, col_idx], Seconds=200, duration=30, ext_title=True, legend=False, x_title=False, y_title=title_list[row_idx]
                    )
                elif row_idx == 0:
                    create_activityplot_subset_subplot(
                        Average_Activity_sub, Average_Activity_rest, color, "blue", 
                        title_h, ax=axes[row_idx, col_idx], Seconds=200, duration=30, ext_title=True, legend=False, x_title=False
                    )
                elif col_idx == 0:
                    create_activityplot_subset_subplot(
                        Average_Activity_sub, Average_Activity_rest, color, "blue", 
                        title_h, ax=axes[row_idx, col_idx], Seconds=200, duration=30, ext_title=False, legend=False, x_title=False, y_title=title_list[row_idx]
                    )
                else:
                    create_activityplot_subset_subplot(
                        Average_Activity_sub, Average_Activity_rest, color, "blue", 
                        title_h, ax=axes[row_idx, col_idx], Seconds=200, duration=30, ext_title=False, legend=False, x_title=False
                    )

    
    # Platz anpassen: mehr Abstand links
    plt.tight_layout()
    plt.subplots_adjust(left=0.12, wspace=0.25, hspace=0.55)  # `left` erhöht Abstand links

    # Gemeinsame Y-Achsenbeschriftungen hinzufügen
    fig.text(0.022, 0.5, 'spiking activity (Hz)', va='center', rotation='vertical', fontsize=22)

    filename = "Spiking.pdf"  # Einfach nur den Dateinamen
    plt.savefig(filename, dpi=300, bbox_inches='tight',  format='pdf')







def moving_average(data, window_size):

    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def avalanche_plot(data, title, col, ax, exponent=-1.5, smoothed=True, window_size=3):
    """
    Plots a histogram with logarithmically distributed bins from 10^0 to 10^6 and normalizes the counts to probabilities.
    Optionally smooths the histogram data using a moving average.
    
    Parameters:
    data (array-like): The data to plot (event sizes).
    ax: Matplotlib axis to draw the plot on.
    smoothed (bool): Whether to apply smoothing to the data.
    window_size (int): The window size for the moving average if smoothing is enabled.
    """
    if len(data) == 0:
        # Beispiel: Hier Power-Law Linie plotten, ohne Datenpunkte (Scatter)
        # Plot der Power-Law-Linie
        # Add reference line for s^-exponent
        ref_x = np.logspace(0, 6, num=50)
        ref_y = ref_x ** exponent
        ax.plot(ref_x, ref_y, 'r--', label=r'$s^{3/2}$')
        return


    # Define logarithmic bins from 10^0 to 10^6
    bin_edges = np.logspace(np.log10(min(data)) - 1, np.log10(max(data)) + 1, num=50)

    
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
    ax.scatter(bin_centers, probabilities, label='Data', c=col, s=5)

    # Set log-log scale
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    # Add reference line for s^-exponent
    ref_x = np.logspace(0, 6, num=50)
    ref_y = ref_x ** exponent
    ax.plot(ref_x, ref_y, 'r--', label=r'$s^{3/2}$')
    
    # Formatting
    ax.set_xlabel('avalanche size s', fontsize=5, labelpad=2)
    #ax.legend(fontsize=5, frameon=False, bbox_to_anchor=(0.9, 1))

    # Customize ticks
    ax.set_xticks([1, 10**2, 10**4, 10**6])
    ax.set_xticklabels([r'$10^0$', r'$10^2$', r'$10^4$', r'$10^6$'], fontsize=6)
    ax.tick_params(axis='y', which='both', labelsize=6)

    # Only left and bottom spines visible
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)


def create_activityplot_subset_subplot(activity_list1: list, activity_list2: list, color_plot1: str, color_plot2: str, h_string: str, ax, Seconds: int = 0, duration: int = 30, ext_title=False, legend=True, x_title=True,  y_title=None):
    # Normalize: Zeitschritte pro Sekunde
    time_steps_per_second = 1000 / 4  # Anzahl der Zeitschritte pro Sekunde

    if Sec > 0:
        # Start- und End-Index basierend auf den Sekunden
        start_index = int(Sec * time_steps_per_second)
        end_index = int((Sec + duration) * time_steps_per_second)

        # Sicherstellen, dass die Indizes im gültigen Bereich liegen
        start_index = max(0, start_index)
        end_index = min(len(activity_list1), end_index)

        # Passenden Bereich auswählen
        x = range(end_index - start_index)
        y1 = activity_list1[start_index:end_index]
        y2 = activity_list2[start_index:end_index]
    else:
        # Gesamte Liste verwenden
        x = range(len(activity_list1))
        y1 = activity_list1
        y2 = activity_list2

    # Zeitpunkte in Sekunden berechnen
    seconds = [i / time_steps_per_second for i in x]

    # Plotte die Aktivitätsdaten
    ax.plot(seconds, y1, color=color_plot1, linewidth=0.3, label='Active')
    ax.plot(seconds, y2, color=color_plot2, linewidth=0.3, label='Passive')

    # X-Achsen-Beschriftungen: nur alle 10 Sekunden
    max_seconds = max(seconds)
    x_tick_positions = list(range(0, int(max_seconds) + 2, 10))  # Alle 10 Sekunden
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels(x_tick_positions, fontsize=6)

    # Y-Achsenlimits und Labels
    ax.set_ylim(0, 40)
    ax.set_yticks([0, 20])
    ax.tick_params(axis='both', labelsize=10)
    if not(y_title == None):
        ax.set_ylabel(y_title, fontsize=9)
    # else:       
    #     ax.set_ylabel(r'$a_t$ (Hz)', fontsize=8, labelpad=20, rotation=0)
    #     ax.yaxis.set_label_position("left")
    #     ax.yaxis.set_label_coords(-0.1, 1.0)
    if x_title:
        ax.set_xlabel('seconds', fontsize=8, labelpad=2)

    # Titel
    if ext_title:
        if not cons.log_r:
            ax.set_title(r'$\frac{h}{r^*} = $' + h_string, color=color_plot1, fontsize=20, pad=20)
        else:
            ax.set_title(r'$\frac{h}{r^*} = $' + h_string + " log_r", color=color_plot1, fontsize=20, pad=20)

    # Nur linke und untere Achsenlinien anzeigen
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # Legende hinzufügen
    if legend:
        ax.legend(loc='upper right', fontsize=3)


def create_activityplot_homogenous(activity_list1: list, color_plot1: str, h_string: str, ax, Seconds: int = 0, duration: int = 30, ext_title=False, legend=True, x_title=True, y_title=None):
    # Normalize: Zeitschritte pro Sekunde
    time_steps_per_second = 1000 / 4  # Anzahl der Zeitschritte pro Sekunde

    if Sec > 0:
        # Start- und End-Index basierend auf den Sekunden
        start_index = int(Sec * time_steps_per_second)
        end_index = int((Sec + duration) * time_steps_per_second)

        # Sicherstellen, dass die Indizes im gültigen Bereich liegen
        start_index = max(0, start_index)
        end_index = min(len(activity_list1), end_index)

        # Passenden Bereich auswählen
        x = range(end_index - start_index)
        y1 = activity_list1[start_index:end_index]
    else:
        # Gesamte Liste verwenden
        x = range(len(activity_list1))
        y1 = activity_list1


    # Zeitpunkte in Sekunden berechnen
    seconds = [i / time_steps_per_second for i in x]

    # Plotte die Aktivitätsdaten
    ax.plot(seconds, y1, color=color_plot1, linewidth=0.3, label='Homogenous')


    # X-Achsen-Beschriftungen: nur alle 10 Sekunden
    max_seconds = max(seconds)
    x_tick_positions = list(range(0, int(max_seconds) + 2, 10))  # Alle 10 Sekunden
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels(x_tick_positions, fontsize=6)

    # Y-Achsenlimits und Labels
    ax.set_ylim(0, 40)
    ax.set_yticks([0, 20])
    ax.tick_params(axis='both', labelsize=10)
    if not(y_title == None):
        ax.set_ylabel(y_title, fontsize=9)
    # else:      
    #     ax.set_ylabel(r'$a_t$ (Hz)', fontsize=8, labelpad=20, rotation=0)
    #     ax.yaxis.set_label_position("left")
    #     ax.yaxis.set_label_coords(-0.1, 1.0)
    if x_title:
        ax.set_xlabel('seconds', fontsize=22, labelpad=7)

    # Titel
    if ext_title:
        if not cons.log_r:
            ax.set_title(r'$\frac{h}{r^*} = $' + h_string, color=color_plot1, fontsize=8, pad=20)
        else:
            ax.set_title(r'$\frac{h}{r^*} = $' + h_string + " log_r", color=color_plot1, fontsize=8, pad=20)

    # Nur linke und untere Achsenlinien anzeigen
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # Legende hinzufügen
    if legend:
        ax.legend(loc='upper right', fontsize=3)





def plot_log_histogram_subplot(data_sub, data_rest, title, col_sub, col_rest, ax, smoothed=True):
    # Define logarithmic bins from 10^0 to 10^6
    bin_edges = np.logspace(0, 6, num=50)

    # Dynamisch berechnete Schriftgrößen basierend auf der Achsgröße
    fig_width, fig_height = ax.figure.get_size_inches()
    label_fontsize = fig_height 
    tick_fontsize_y = fig_height 
    tick_fontsize_x = fig_height 

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
            ax.scatter(smoothed_bin_centers, smoothed_probabilities, label=f'Smoothed {label}', color=color, s=5)
        else:
            ax.scatter(bin_centers, probabilities, label=label, color=color, s=5)

    # Plot data for sub and rest datasets
    plot_data(data_sub, label='Sub', color=col_sub, bin_edges=bin_edges)
    plot_data(data_rest, label='Rest', color=col_rest, bin_edges=bin_edges)

    # Set log-log scale
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Add reference line for s^-3/2
    ref_x = np.logspace(0, 6, num=50)
    ref_y = ref_x ** (-3 / 2)
    ax.plot(ref_x, ref_y, 'r--', label=r'$P(s) = s^{-3/2}$')

    # Hide all spines, then make only the left and bottom axes visible
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # Labels and title
    ax.set_xlabel('avalanche size s', fontsize=5)
    #ax.set_ylabel('Avalanche\nDistribution', fontsize=5, labelpad=10)
    #ax.set_title(title, color=col_sub, fontsize=fig_height * 8, pad=15)
    #ax.legend(fontsize=6)

    # Customizing tick fonts
    ax.set_xticks([10**i for i in [0, 2, 4, 6]])  # Set specific x-ticks
    ax.set_xticklabels([r'$10^0$', r'$10^2$', r'$10^4$', r'$10^6$'], fontsize=tick_fontsize_x)
    ax.tick_params(axis='y', labelsize=tick_fontsize_y)



def moving_average(data, window_size):
    """A simple moving average function for smoothing."""
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def avalanche_plot_single(AVA_DIST_LIST, H_LIST, COLOR_LIST, ax=None, title=None, exponent=-3/2, smoothed=True, window_size=5):
    """
    Plots multiple avalanche size distributions on a single log-log plot.
    
    Parameters:
    AVA_DIST_LIST (list of array-like): List of avalanche distributions to plot.
    H_LIST (list of str): List of titles for the legend corresponding to each dataset.
    COLOR_LIST (list of str): List of colors for each dataset.
    ax (matplotlib.axes.Axes): Existing axis to draw on. If None, creates a new figure.
    title (str): Title of the plot (optional).
    exponent (float): Exponent for the reference line (default is -3/2).
    smoothed (bool): Whether to apply smoothing to the data.
    window_size (int): The window size for the moving average if smoothing is enabled.
    """
    # Create figure and axis if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))  # Create a new figure and axis if ax is None

    # Iteration through the data lists
    for data, h_title, color in zip(AVA_DIST_LIST, H_LIST, COLOR_LIST):
        # Wenn die Daten leer sind, fügen wir einen sehr großen Wert hinzu
        if len(data) == 0:
            data = [1000000000]  # Ein Wert, der auf dem Plot nicht sichtbar ist

        bin_edges = np.logspace(np.log10(min(data)) - 1, np.log10(max(data)) + 1, num=100)
        
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
        
        # Vergewissern, dass bin_centers und probabilities die gleiche Länge haben
        if len(bin_centers) == len(probabilities) and len(bin_centers) > 0:
            # Plot the histogram on a log-log scale
            ax.scatter(bin_centers, probabilities, label=h_title, c=color, s=60)
        else:
            print(f"Skipping plot for {h_title}: unequal bin_centers and probabilities lengths")

    # Set log-log scale
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Customize ticks
    ax.set_xticks([1, 10**2, 10**4, 10**6])
    ax.set_xticklabels([r'$10^0$', r'$10^2$', r'$10^4$', r'$10^6$'], fontsize=20)
    ax.tick_params(axis='y', which='both', labelsize=20)

    # Only left and bottom spines visible
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # Add reference line for s^-exponent
    ref_x = np.logspace(0, 6, num=50)
    ref_y = ref_x ** exponent
    ax.plot(ref_x, ref_y, 'r--', label=r'$s^{3/2}$')

    # Add title and legend
    if title:
        ax.set_title(title, fontsize=20, pad=10)
    ax.legend(fontsize=12, frameon=False)

    # Layout adjustment only if a new figure is created
    if ax is None:
        fig.tight_layout()
        plt.show()

    return ax  # Return the axis if it's created




def create_two_multiplot(data_list, title_list, main_title=None, figsize=(10, 10)):
    """
    Creates a layout with four avalanche size distribution plots in a 2x2 grid.

    Parameters:
    data_list (list of tuples): List containing (AVA_DIST_LIST, H_LIST, COLOR_LIST) for each dataset.
    title_list (list of str): List of titles for each subplot.
    main_title (str): Optional main title of the plot.
    figsize (tuple): Size of the figure.
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)  # 2x2-Grid von Plots
    axes = axes.flatten()  # Flach machen für einfachere Iteration

    # Für jede Eingabe einen Plot erstellen
    for idx, (ax, (AVA_DIST_LIST, H_LIST, COLOR_LIST), title) in enumerate(zip(axes, data_list, title_list)):
        avalanche_plot_single(AVA_DIST_LIST, H_LIST, COLOR_LIST, ax=ax, title=title, smoothed=True)

        # Nur für die linke Spalte die y-Achsenbeschriftung hinzufügen
        if idx % 2 == 0:  # Linke Spalte hat Index 0 und 2
            ax.set_ylabel("Probability", fontsize=25)
        if idx in [2,3]:  # Linke Spalte hat Index 0 und 2
            ax.set_xlabel("avalanche size s", fontsize=25)

    # Haupttitel optional
    if main_title:
        fig.suptitle(main_title, fontsize=20, y=1.02)
    fig.tight_layout()
    filename = "Avalanche_Classic.pdf"  # Einfach nur den Dateinamen
    plt.savefig(filename, dpi=300, bbox_inches='tight', format='pdf')







import sys 
sys.path.append("/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit")

from Models import Bachelor_Collection as BC







data_list = [
    AA_Plot(BC.SC_Subset_Centered_Classic, homogenous=False),
    AA_Plot(BC.SC_Subset_Random_Classic, homogenous=False),      # Daten für dritten Plot
    AA_Plot(BC.SC_Homogenous_Classic, homogenous=True),  # Daten für zweiten Plot
    AA_Plot(BC.ER_Subset_Classic, homogenous=False)       # Daten für dritten Plot
]

Runs = [
    BC.SC_Subset_Centered_Classic[::-1],  # Daten für die erste Reihe umkehren
    BC.SC_Subset_Random_Classic[::-1],    # Daten für die zweite Reihe umkehren
    BC.ER_Subset_Classic[::-1],           # Daten für die vierte Reihe umkehren
    BC.SC_Homogenous_Classic[::-1]        # Daten für die dritte Reihe umkehren
]

Spiking_Plot(Runs)


# Titel für die Subplots
title_list = [
    "Spacial Clustered\nSubset Centered", 
    "Spacial Clustered\nSubset Random",
    "Spacial Clustered\nHomogenous",
    "Erdos Renyi\nSubset"
]

# Haupttitel
main_title = "Avalanche Size Distribution"

# Multiplot erstellen
create_two_multiplot(data_list, title_list)

