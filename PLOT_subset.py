import pickle
import os
import sys
import numpy as np
# append parent directory for importing constants
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
from Functions_Constants_Meters import Constants as cons
from Models import Bachelor_Collection as BC


#  -------------------------------  Please Change ---------------------------------
Sec = 0 # Change this to get a different cutout of the spiking activity. set to 0 to see the whole run.
path = "/Users/johanneswalka/Documents/Zeug/Anderes_Zeugs/Implementierung_Bachelorarbeit_3/Runtime_Data/SC_Compiled10000_Centered_1_0.001_2_500_1.pkl" # put here the path to the pkl. of your run. You find it in "Runtime_Data



with open(path, 'rb') as file:
    data_dict = pickle.load(file)



# Beispiel für den Zugriff auf die einzelnen Listen
h = data_dict["h"]
model =  data_dict["model"]
n =  data_dict["N"]
Alpha_init = data_dict["Alpha_init"]      
Targetrate =  data_dict["Targetrate"]     
Homeo_con =  data_dict["Homeo_con"]  
Seconds = data_dict["Sec"]    
# Global Act is actually the individual branching parameter, used because of infrastructur already existiing
global_act = data_dict["global_act"]
branching_global = data_dict["Branching_global"]
autocorrelation = data_dict["Autocorrelation"]
Avalanche_Distribution = data_dict["Avalanche_Distribution"]
sec = data_dict["Sec"]


Average_Activity_rest = data_dict["Average_Activity_rest"]
Average_Activity_sub = data_dict["Average_Activity_sub"]
Average_Alpha_sub = data_dict["Average_Alpha_sub"]
Average_Alpha_rest = data_dict["Average_Alpha_rest"]


title_h, color = BC.get_h_col(h)




# plot the average Activity
from RESEARCH_Subset import ActivityPlot_Subset as act_plot_sub
act_plot_sub.create_activityplot_subset(Average_Activity_sub, Average_Activity_rest, color, title_h, Sec)

# Avalanche plot 
from Ploting import AvalanchePlot as ava_plot
ava_plot.plot_log_histogram(Avalanche_Distribution, r'$\frac{h}{r^*} = $' + title_h, color)


# # Print the specifics used in the model
print("")
print("Used Modell: ", model)
print("Number of Neurons: ", n)
print("Running Time: ", Seconds)
print("Input rate h:", h)
print("Target Spiking Rate: ", Targetrate)
print("Homeostatic Constant: ", Homeo_con)
print("Alpha init: ", Alpha_init)




