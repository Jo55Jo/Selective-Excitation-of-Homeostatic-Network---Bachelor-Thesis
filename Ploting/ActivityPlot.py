import matplotlib.pyplot as plt 
import numpy as np
from Functions_Constants_Meters import Constants as cons
import os

# Subplot-Konfigurationseinstellungen
plt.rcParams['figure.subplot.left'] = 0.2
plt.rcParams['figure.subplot.right'] = 0.9
plt.rcParams['figure.subplot.bottom'] = 0.25
plt.rcParams['figure.subplot.top'] = 0.7
plt.rcParams['figure.subplot.wspace'] = 0.2
plt.rcParams['figure.subplot.hspace'] = 0.2

def create_activityplot(activity_list: list, color_plot: str, h_string: str, Sec: int = 0):
    # Erstellen der Figur und Zugriff auf ihre Größe
    fig = plt.figure(figsize=(4, 4), dpi=200)
    fig_width, fig_height = fig.get_size_inches()

    # Dynamisch berechnete Schriftgrößen basierend auf der Plotgröße
    title_fontsize = fig_height * 8
    label_fontsize = fig_height * 7
    tick_fontsize_y = fig_height * 8.0  
    tick_fontsize_x = fig_height * 5

    # X-Achse: Zeit in diskreten Zeitschritten
    x = range(len(activity_list))
    y = activity_list

    # Normalize (1000 Zeitschritte) und geteilt durch 4 für die mittlere Aktivität
    normalize = 1000 / 4

    # Falls Sec angegeben ist, 30-Sekunden Intervall ab Sec auswählen
    if Sec > 0:
        start_index = int(Sec * normalize)
        end_index = int((Sec + 30) * normalize)
        x = range(start_index, end_index)
        y = activity_list[start_index:end_index]
        
        # Labels für 10, 20, 30 Sekunden
        x_tick_labels = [i * 10 for i in range(4)]
        x_tick_positions = [start_index + i * int(normalize * 10) for i in range(4)]
        plt.xticks(ticks=x_tick_positions, labels=x_tick_labels, fontsize=tick_fontsize_x)
    else:
        # Festgelegte x-Ticks in 10er-Schritten für die gesamte Zeitreihe
        x_tick_positions = [int(i * normalize * 10) for i in range(len(x) // int(normalize * 10) + 1)]
        x_tick_labels = [i * 10 for i in range(len(x_tick_positions))]
        plt.xticks(ticks=x_tick_positions, labels=x_tick_labels, fontsize=tick_fontsize_x)

    # Plot
    print(len(x), len(y))
    plt.plot(x, y, color=color_plot, linewidth=1)

    # Nur die linke und untere Achse sichtbar machen
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.gca().spines['left'].set_visible(True)
    plt.gca().spines['bottom'].set_visible(True)

    # X- und Y-Achsenbeschriftungen
    plt.xlabel('Seconds', fontsize=label_fontsize, fontweight=500)
    plt.ylabel(r'$a_t$ (Hz)', fontsize=label_fontsize-6, fontweight=500, labelpad=20, rotation=0)  
    plt.gca().yaxis.set_label_position("left")
    plt.gca().yaxis.set_label_coords(0.05, 1.0)
    plt.ylim(0, 40)
    plt.yticks([0, 20], fontsize=tick_fontsize_y)

    # Titel hinzufügen
    if not cons.log_r:
        plt.title(r'$\frac{h}{r^*} = $' + h_string, color=color_plot, fontsize=title_fontsize, pad=45, fontweight='bold')
    else:
        plt.title(r'$\frac{h}{r^*} = $' + h_string + " log_r", color=color_plot, fontsize=title_fontsize, pad=40)

    # Plot speichern
    output_dir = "Ploting/plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    base_filename = "Activity"
    file_extension = ".png"
    counter = 1
    output_file = os.path.join(output_dir, base_filename + file_extension)
    while os.path.exists(output_file):
        output_file = os.path.join(output_dir, f"{base_filename}_{counter}{file_extension}")
        counter += 1
    plt.savefig(output_file)

    # Diagramm anzeigen
    plt.show()
