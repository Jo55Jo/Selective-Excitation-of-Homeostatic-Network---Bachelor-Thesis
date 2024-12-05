import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pickle
import os
import sys
import numpy as np
import numpy as np
import pickle
# append parent directory for importing constants
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
print(parent_dir)
sys.path.append(parent_dir)
from Models import Bachelor_Collection as BC
from Functions_Constants_Meters import Constants as cons




# Set true for plot of the subset/rest branching parameters and false for network branching parameters
Subset = True

# In the thesis runs, data was collected during the burninperiod. Therefore only values after that period were used
Thesis_Run = True

#TITLE = ["SC-Subset-Centered", "SC-Subset-Random", "SC-Homogenous", "ER-Subset"]
TITLE = ["SC-Subset-Centered-Subset", "SC-Subset-Centered-Rest", "SC-Random-Subset", "Sc-Random-Rest", "ER-Subset", "ER-Rest"]


COMPLETE_BRANCHING = []
# Gibt an, wie sicher sich der Test ist, das Alpha der richtige Exponent ist. 
COMPLETE_SD = []
COMPLETE_H = []
COMPLETE_RUNS = []
# Kolmogorov-Smirnov (KS)-Test gibt an, wie gut die Daten dazu passen. 
COMPLETE_P_VALUE = []

if Subset:
    BC.SC_Subset_Centered_Complete.reverse()
    COMPLETE_RUNS.append(BC.SC_Subset_Centered_Complete)

    BC.SC_Subset_Random_Complete.reverse()
    COMPLETE_RUNS.append(BC.SC_Subset_Random_Complete)

    BC.ER_Subset_Complete.reverse()
    COMPLETE_RUNS.append(BC.ER_Subset_Complete)

else:
    BC.SC_Subset_Centered_Complete.reverse()
    COMPLETE_RUNS.append(BC.SC_Subset_Centered_Complete)

    BC.SC_Subset_Random_Complete.reverse()
    COMPLETE_RUNS.append(BC.SC_Subset_Random_Complete)

    BC.SC_Homogenous_Complete.reverse()
    COMPLETE_RUNS.append(BC.SC_Homogenous_Complete)

    BC.ER_Subset_Complete.reverse()
    COMPLETE_RUNS.append(BC.ER_Subset_Complete)




for e, Condition in enumerate(COMPLETE_RUNS):
    BRANCHING = []
    BRANCHING_SUB = []
    BRANCHING_REST = []
    SD = []
    SD_SUB = []
    SD_REST = []
    H = []


    #plt.figure(figsize=(10,8))
    for i, run in enumerate(Condition):

        cons.Subset = True
        with open(run, 'rb') as file:
            data_dict = pickle.load(file)
        # Beispiel für den Zugriff auf die einzelnen Listen
        h = data_dict["h"]
        branching_global = data_dict["Branching_global"]
        Branching_Individual = data_dict["global_act"]

        #print(TITLE[i], len(branching_global))


        if Subset:
            if Thesis_Run:
                Branch_sub = [np.average(i[:500]) for i in Branching_Individual]
                Branch_rest = [np.average(i[500:]) for i in Branching_Individual]


                total_average = np.average(branching_global[5000:])
            else:
                Branch_sub = [np.average(i) for i in Branching_Individual]
                Branch_rest = [np.average(i) for i in Branching_Individual]


                total_average = np.average(branching_global)
            

            b_sub_average = np.average(Branch_sub)
            b_sub_sd = np.std(Branch_sub)
            print(i, "branching", b_sub_sd)
            
            b_rest_average = np.average(Branch_rest)
            b_rest_sd = np.std(Branch_rest)
            print(i, "branching rest", b_rest_sd)


            #Collecting the Data
            BRANCHING_SUB.append(b_sub_average)
            BRANCHING_REST.append(b_rest_average)

            SD_SUB.append(b_sub_sd)
            SD_REST.append(b_rest_sd)
            H.append(h)


        else:
            if Thesis_Run:
                if e == 2:
                    total_average = np.average(branching_global[125500:])
                    total_sd = np.std(branching_global[125500:])
                else:
                    total_average = np.average(branching_global[5000:])
                    total_sd = np.std(branching_global[5000:])
            else:
                if e == 2:
                    total_average = np.average(branching_global)
                    total_sd = np.std(branching_global)
                else:
                    total_average = np.average(branching_global)
                    total_sd = np.std(branching_global)
            #Collecting the Data
            BRANCHING.append(total_average)
            SD.append(total_sd)
            H.append(h)
            


    if Subset:
        COMPLETE_BRANCHING.append(BRANCHING_SUB)
        COMPLETE_BRANCHING.append(BRANCHING_REST)
        COMPLETE_SD.append(SD_SUB)
        COMPLETE_SD.append(SD_REST)
        COMPLETE_H.append(H)
        COMPLETE_H.append(H)


    else:
        COMPLETE_BRANCHING.append(BRANCHING)
        COMPLETE_SD.append(SD)
        COMPLETE_H.append(H)








import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
def Branching_Comparison(Branching, h, TITLE, SD, Subset=False):
    """
    Plots multiple lines with standard deviation (SD) as error bars on a logarithmic X-axis.

    Parameters:
        Branching (list of lists): Y-values for each line.
        sigma (list of lists): Standard deviation for each line.
        legend_titles (list of str): Titles for the legend.
        x_values (list of lists): X-values corresponding to each line.
    """
    plt.figure(figsize=(10, 6))
    
    if not Subset:
        color = ['blue', 'lightblue', 'green', 'red']

        for i in range(len(Branching)):

            h_string, Fisch = BC.get_h_col(h[i])
            x = np.array(h[i])
            y = np.array(Branching[i])
            sd = np.array(SD[i])
            # Plot the line
            plt.plot(x, y, label=TITLE[i], color=color[i])
            # Add error bars for SD
            plt.errorbar(x, y, yerr=sd, fmt='o', color=color[i], ecolor=color[i], capsize=3, elinewidth=1, capthick=1)

    # What if it was Subset Condition 
    if Subset:
        color = ['blue', 'lightblue', 'green', 'lightgreen', 'red', 'pink']



        for i in range(len(Branching)):

            h_string, Fisch = BC.get_h_col(h[i])
            print(i)
            print("h:", len(h))
            print("SD:", len(SD))
            print("Color:", len(color))
            print("Title:", len(TITLE))
            print("branch:", len(Branching))
        
            x = np.array(h[i])
            y = np.array(Branching[i])
            sd = np.array(SD[i])
            print(sd)
            # Plot the line
            print(i)
            print(len(TITLE))
            print(len(color))
            print(len(Branching))
            plt.plot(x, y, label=TITLE[i], color=color[i])
            
            # Add error bars for SD
            plt.errorbar(x, y, yerr=sd, fmt='o', color=color[i], ecolor=color[i], capsize=3, elinewidth=1, capthick=1)


    # Set X-axis to logarithmic scale
    plt.xscale('log')

    # Set X-ticks only at specific values
    unique_x_values = sorted(set(val for sublist in h for val in sublist))
    plt.xticks(
        unique_x_values, 
        [f"$10^{{{int(np.log10(val))}}}$" if val in [1e-4, 1e-3, 1e-2, 1e-1, 1e-0] else "" for val in unique_x_values],
        fontsize = 20
    )

    # Set y-axis limits and ticks
    plt.ylim(0.5, 1.3)
    plt.yticks(np.arange(0.6,1.2,0.2), fontsize=15)  # y-labels bei Schritten von 0.1

    plt.xlabel("External Input (h)", fontsize=25, labelpad=10)
    if Subset:
        plt.ylabel(r"Subset/Rest ($m_t)$", fontsize=18, labelpad=10)
    else:
        plt.ylabel(r"Network Branching Parameter ($m_t$)", fontsize=18, labelpad=10)

    if Subset:
        plt.title(r"Subset/Rest ($m_t$)", fontsize=30)    
    else:
        plt.title(r"Network Branching ($m_t$)", fontsize=30)
    plt.legend()
    plt.grid(True, which="both", linestyle='--', alpha=0.6)  # Grid für Major und Minor Ticks
    plt.tight_layout()
    plt.show()




Branching_Comparison(COMPLETE_BRANCHING, COMPLETE_H, TITLE, COMPLETE_SD, Subset=True)