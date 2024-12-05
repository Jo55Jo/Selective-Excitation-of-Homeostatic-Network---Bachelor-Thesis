import matplotlib.pyplot as plt 
import numpy as np
from Functions_Constants_Meters import Constants as cons
import os

# Subplot-Konfigurationseinstellungen
plt.rcParams['figure.subplot.left'] = 0.25
plt.rcParams['figure.subplot.right'] = 0.9
plt.rcParams['figure.subplot.bottom'] = 0.2
plt.rcParams['figure.subplot.top'] = 0.9
plt.rcParams['figure.subplot.wspace'] = 0.2
plt.rcParams['figure.subplot.hspace'] = 0.2

def plot_homeostatic(homeo_1: list, color_plot: str, h_string: str, N: int, seconds: int):
    # Erstellen der Figur und Zugriff auf ihre Größe
    fig = plt.figure(figsize=(4, 3), dpi=200)
    fig_width, fig_height = fig.get_size_inches()

    # Dynamisch berechnete Schriftgrößen basierend auf der Plotgröße
    title_fontsize = fig_height * 7  
    label_fontsize = fig_height * 5   
    tick_fontsize_y = fig_height * 5.0    
    tick_fontsize_x = fig_height * 5  

    # X-Achse: Zeit in diskreten Zeitschritten (Sekunden / delta_t)
    x = range(len(homeo_1))
    normalize = 1000 / 4
    y = homeo_1

    # Größter und kleinster Wert aus der Liste
    max_value = max(homeo_1)
    min_value = min(homeo_1)




    # Achsen anpassen
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.gca().spines['left'].set_visible(True)
    plt.gca().spines['bottom'].set_visible(True)

    # X-Achsenbeschriftung
    plt.xlabel('Seconds', fontsize=label_fontsize, fontweight=500)

    # Y-Achsenbeschriftung und Begrenzungen
    plt.ylabel(r"$\overline{\alpha}$", fontsize=label_fontsize, fontweight=500, labelpad=20, rotation=0)  
    plt.gca().yaxis.set_label_position("left")
    plt.gca().yaxis.set_label_coords(0.01, 1.02)  
    plt.ylim(min_value - 0.01, max_value + 0.01)

    # Y-Achse bei spezifischen Werten beschriften
    y_ticks = [min_value - 0.005, (min_value + max_value) / 2, max_value + 0.005]
    plt.yticks(y_ticks, labels=[f'{tick:.3f}' for tick in y_ticks], fontsize=tick_fontsize_y)

    # Custom x-ticks für Anfang und Ende
    x_tick_positions = [0, len(x) - 1]
    x_tick_labels = [int(pos / normalize) for pos in x_tick_positions]
    plt.xticks(ticks=x_tick_positions, labels=x_tick_labels, fontsize=tick_fontsize_x)

    plt.plot(x, y, color=color_plot, linewidth=1)

    # Plot speichern
    output_dir = "Ploting/plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    base_filename = "Homeostatic"
    file_extension = ".png"

        # Finde einen nicht vorhandenen Dateinamen durch Anhängen einer Zahl
    counter = 1
    output_file = os.path.join(output_dir, base_filename + file_extension)
    while os.path.exists(output_file):
        output_file = os.path.join(output_dir, f"{base_filename}_{counter}{file_extension}")
        counter += 1

    # Speichere das Plot im angegebenen Verzeichnis
    plt.savefig(output_file)

    # Diagramm anzeigen
    plt.show()  
   
