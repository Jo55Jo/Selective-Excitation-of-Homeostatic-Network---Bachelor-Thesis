import pickle
import os
import sys
import powerlaw as pow
import numpy as np
import matplotlib.pyplot as plt



# append parent directory for importing constants
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

from Functions_Constants_Meters import Constants as cons
from Models import Bachelor_Collection as BC 
import numpy as np
import matplotlib.pyplot as plt





# Finite_Effect used in thesis
Finite_Effect = True

TITLES = ["SC-Subset-Centered", "SC-Subset-Random", "SC-Homogenous", "ER-Subset"]
#TITLES.reverse()

COMPLETE_ALPHA = []
# Gibt an, wie sicher sich der Test ist, das Alpha der richtige Exponent ist.
COMPLETE_SIGMA = []
COMPLETE_H = []
COMPLETE_RUNS = []
# Kolmogorov-Smirnov (KS)-Test gibt an, wie gut die Daten dazu passen. 
COMPLETE_D = []
COMPLETE_P_VALUES = []

COMPLETE_AVALANCHE_SAMPLE_LENGTH = []


BC.SC_Subset_Centered_Complete.reverse()
COMPLETE_RUNS.append(BC.SC_Subset_Centered_Complete)

BC.SC_Subset_Random_Complete.reverse()
COMPLETE_RUNS.append(BC.SC_Subset_Random_Complete)

BC.SC_Homogenous_Complete.reverse()
COMPLETE_RUNS.append(BC.SC_Homogenous_Complete)

BC.ER_Subset_Complete.reverse()
COMPLETE_RUNS.append(BC.ER_Subset_Complete)

for Condition in COMPLETE_RUNS:
    ALPHA = []
    SIGMA = []
    XMIN = []
    H = []
    KOL_D = []
    AVALANCHE_SAMPLE_LENGTH = []

    for i, run in enumerate(Condition):
        print(i)
        cons.Subset = True
        with open(run, 'rb') as file:
            data_dict = pickle.load(file)
        # Beispiel für den Zugriff auf die einzelnen Listen
        h = data_dict["h"]
        data = data_dict["Avalanche_Distribution"]
        #statistic, p_value = kstest(data, cdf="powerlaw")


        if Finite_Effect:
            data = [x for x in data if 0 < x < 10000]


        h_string, color = BC.get_h_col(h)
        # Doing the Fit    
        '''
        Fit = pow.Fit(data)
        alpha = float(Fit.power_law.alpha)
        xmin = Fit.power_law.xmin
        sigma = Fit.power_law.sigma
        '''
        Fit = pow.Fit(data)
        xmin = Fit.xmin


        if xmin > 1000:
            print("h for x min > 100::::::::: ", h)
            Fit_xmin = pow.Fit(data, xmin=1)
            alpha = float(Fit_xmin.power_law.alpha)
            xmin = Fit_xmin.power_law.xmin
            sigma = Fit_xmin.power_law.sigma
            kol_d = Fit_xmin.power_law.D

            

        else:
            alpha = float(Fit.power_law.alpha)
            xmin = Fit.power_law.xmin
            sigma = Fit.power_law.sigma
            kol_d = Fit.power_law.D


        print(kol_d)
        #Collecting the Data
        ALPHA.append(alpha)
        SIGMA.append(sigma)
        KOL_D.append(kol_d)
        XMIN.append(xmin)
        H.append(h)

        AVALANCHE_SAMPLE_LENGTH.append(len(data))

        # printing some stuff
        '''
        print("")
        print("")
        print("")
        print(f"h: {h}")
        print(f"Optimaler Alpha: {alpha}")
        print(f"Optimaler xmin: {xmin}")
        print(f"sd: {sigma}")
        '''
    # Figure1.tick_params(axis='x', labelsize=15)  # X-Tick-Labels auf Größe 15
    # Figure1.tick_params(axis='y', labelsize=15)
    # plt.tight_layout()
    # plt.show()
    
    COMPLETE_ALPHA.append(ALPHA)
    COMPLETE_SIGMA.append(SIGMA)
    COMPLETE_H.append(H)
    COMPLETE_D.append(KOL_D)
    COMPLETE_AVALANCHE_SAMPLE_LENGTH.append(AVALANCHE_SAMPLE_LENGTH)
    #COMPLETE_P_VALUES.append(P_VALUES)

        #print("")
        #print("H: ", h)
        #ava_plot.plot_log_histogram(data, "lala", "blue", -3/2)
        #alpha, Squared_error = fit_power_law(data, xmin=0, xmax=1000000000)
        #print(f"Geschätzter Power-Law-Exponent (Alpha): {alpha}")
        #print("Squared Error: ", Squared_error)




import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def alpha_kolmo(alpha, sigma, legend_titles, x_values, Kolmogorov_D):
    """
    Plots multiple lines with standard deviation (SD) as error bars on a logarithmic X-axis.

    Parameters:
        alpha (list of lists): Y-values for each line.
        sigma (list of lists): Standard deviation for each line.
        legend_titles (list of str): Titles for the legend.
        x_values (list of lists): X-values corresponding to each line.
    """
    plt.figure(figsize=(10, 6))

    colors = ['blue', 'lightblue', 'green', 'red']
    #colors.reverse()

    for i in range(len(alpha)):
        x = np.array(x_values[i])
        y = np.array(alpha[i])
        D = np.array(Kolmogorov_D[i])
        print(f"{TITLES[i]}: {D}")
        # Plot the line
        plt.plot(x, y, label=legend_titles[i], color=colors[i])
        
        # Add error bars for SD
        plt.errorbar(x, y, yerr=D, fmt='o', color=colors[i], ecolor=colors[i], capsize=3, elinewidth=1, capthick=1, uplims=False, lolims=True)

    # Set X-axis to logarithmic scale
    plt.xscale('log')

    # Set X-ticks only at specific values
    unique_x_values = sorted(set(val for sublist in x_values for val in sublist))
    plt.xticks(
        unique_x_values, 
        [f"$10^{{{int(np.log10(val))}}}$" if val in [1e-4, 1e-3, 1e-2, 1e-1, 1e0] else "" for val in unique_x_values],
        fontsize = 20
    )

    # Set y-axis limits and ticks
    plt.ylim(1.30, 1.70)
    plt.yticks(np.arange(1.30, 1.71, 0.1), fontsize=15)  # y-labels bei Schritten von 0.1

    plt.xlabel("External Input (h)", fontsize=25, labelpad=10)
    plt.ylabel(r"Alpha, $\uparrow$ = Kol_Dist", fontsize=25, labelpad=10)
    plt.title("Powerlaw-Fit", fontsize=30)
    plt.legend()
    plt.grid(True, which="both", linestyle='--', alpha=0.6)  # Grid für Major und Minor Ticks
    plt.tight_layout()
    plt.show()


from scipy.stats import kstwobign


COMPLETE_P_VALUES = []
for i, run in enumerate(COMPLETE_D):
    P_VALUES = []
    for e, D in enumerate(run):
        n = COMPLETE_AVALANCHE_SAMPLE_LENGTH[i][e]
        print(f"Run {i}, Sample {e}, D: {D}, n: {n}")

        # Berechnung der p-Wert
        p_value = kstwobign.sf(D * (n ** 0.5))  # survival function = 1 - cdf
        P_VALUES.append(p_value)
    COMPLETE_P_VALUES.append(P_VALUES)


for i in range(len(TITLES)):
    # Werte von np.float64 in reguläre Floats umwandeln und runden
    formatted_values = [round(float(value), 4) for value in COMPLETE_P_VALUES[i]]
    print(f"{TITLES[i]} - KS-TEST: {formatted_values}")




for i in range(len(TITLES)):
    # Werte von np.float64 in reguläre Floats umwandeln und runden
    formatted_values = [round(float(value), 4) for value in COMPLETE_ALPHA[i]]
    print(f"{TITLES[i]} - Alpha: {formatted_values}")

for i in range(1, len(TITLES)):
    # Werte von np.float64 in reguläre Floats umwandeln und runden
    SC_SC = [round(float(value), 4) for value in COMPLETE_D[0]]
    Other = [round(float(value), 4) for value in COMPLETE_D[i]]
    
    # Elementweises Teilen der Listen
    Ratio = [round(sc / other, 4) if other != 0 else float('inf') for sc, other in zip(SC_SC, Other)]
    
    # Optional: Ergebnis ausgeben oder weiter verarbeiten
    print(f"Ratio für SC_SC/{TITLES[i]}: {Ratio}")






# Funktion aufrufen
alpha_kolmo(COMPLETE_ALPHA, COMPLETE_SIGMA, TITLES, COMPLETE_H, COMPLETE_D)