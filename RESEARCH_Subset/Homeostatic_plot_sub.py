import matplotlib.pyplot as plt 
import numpy as np
from Functions_Constants_Meters import Constants as cons
import os


# Subplot-Konfigurationseinstellungen
plt.rcParams['figure.subplot.left'] = 0.265
plt.rcParams['figure.subplot.right'] = 0.623
plt.rcParams['figure.subplot.bottom'] = 0.27
plt.rcParams['figure.subplot.top'] = 0.64
plt.rcParams['figure.subplot.wspace'] = 0.2
plt.rcParams['figure.subplot.hspace'] = 0.2

import os
import matplotlib.pyplot as plt

def plot_homeostatic_subset(homeo_1: list, homeo_2: list, color_plot: str, h_string: str, N: int):
    # Erstellen der Figur und Zugriff auf ihre Größe
    fig = plt.figure(figsize=(6, 3), dpi=200)
    fig_width, fig_height = fig.get_size_inches()

    # Dynamisch berechnete Schriftgrößen basierend auf der Plotgröße
    title_fontsize = fig_height * 7  # Beispiel: 13.3 mal die Höhe der Figur
    label_fontsize = fig_height * 5   # Beispiel: 8.3 mal die Höhe der Figur
    tick_fontsize_y = fig_height * 5.0    # Beispiel: 5.0 mal die Höhe der Figur
    tick_fontsize_x = fig_height * 3.0    # Beispiel: 5.0 mal die Höhe der Figur

    # X-Achse: Zeit in diskreten Zeitschritten (Sekunden / delta_t)
    x = range(len(homeo_1))
    # Normalize because delta_t is 4 for average activity in the paper
    normalize = 1000 / 4

    # Y-Achse: Aktivitätswerte
    y1 = homeo_1
    y2 = homeo_2

    # get the mean of homeostatic array 
    # Größter Wert aus beiden Listen
    max_value = max(max(homeo_1), max(homeo_2))
    min_value = min(min(homeo_1), min(homeo_2))

    # Plotte die erste Liste (Group1)
    plt.plot(x, y1, color=color_plot, linewidth=1, label='Active')

    # Plotte die zweite Liste (Group2) in Schwarz
    plt.plot(x, y2, color='black', linewidth=1, label='Passive')

    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    # Nur die linke und untere Achse sichtbar machen
    plt.gca().spines['left'].set_visible(True)
    plt.gca().spines['bottom'].set_visible(True)

    # X-Achse festlegen
    plt.xlabel('Seconds', fontsize=label_fontsize, fontweight=500)

    # Y-Achse festlegen und Maximum auf 40 setzen
    plt.ylabel('Alpha', fontsize=label_fontsize, fontweight=500, labelpad=20, rotation=0)  
    plt.gca().yaxis.set_label_position("left")
    plt.gca().yaxis.set_label_coords(0.05, 1.0)  # Position der Y-Achsenbeschriftung anpassen
    plt.ylim(min_value-0.01, max_value+0.01)  # Setze das Maximum der Y-Achse auf 40

    # Y-Achse nur bei 20 und 40 beschriften
    plt.yticks(np.arange(min_value-0.01, max_value+0.01, step = 0.01), fontsize=tick_fontsize_y)
    
    
    # Set custom x-ticks to display only integer labels
    if cons.Seconds < 10:
        x_tick_positions = [i for i in range(len(x)+1) if i / normalize % 1 == 0]  # Plotte nur X-Werte, die ganze Zahlen sind
    else:
        x_tick_positions = [i for i in range(len(x)+1) if i / normalize % 10 == 0]  # Plotte nur X-Werte, die ganze Zahlen sind
    
    '''
    # Set custom x-ticks to display only integer labels
    if cons.Seconds < 10:
        x_tick_positions = [i for i in range(len(x)+1) if i / normalize % 1 == 0]  # Plotte nur X-Werte, die ganze Zahlen sind
    elif cons.Seconds < 100:
        x_tick_positions = [i for i in range(len(x)+1) if i / normalize % 10 == 0]  # Plotte nur X-Werte, die ganze Zahlen sind
    else:
        x_tick_positions = [i for i in range(len(x)+1) if i / normalize % 100 == 0]  # Plotte nur X-Werte, die ganze Zahlen sind
    '''

    x_tick_labels = [int(pos / normalize) for pos in x_tick_positions]
    plt.xticks(ticks=x_tick_positions, labels=x_tick_labels, fontsize=tick_fontsize_x)

    # Titel hinzufügen
    plt.title(r'$\frac{h}{r^*} = $' + h_string, color=color_plot, fontsize=title_fontsize, pad=40, fontweight='bold')

    # Legende hinzufügen
    plt.legend(loc='upper right', fontsize='small')

    # Saving the Plot in a plots directory
    output_dir = "Ploting/plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Basis-Dateiname ohne Erweiterung
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
