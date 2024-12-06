from Ploting import ActivityPlot as act_plot
from Functions_Constants_Meters import Constants as cons
import Runtime_Data.Make_RuntimeData as rd
import Run_Model_BurnIn as BurnIn

# if its tests, cons.Subset should be false
cons.Subset = False
cons.Fluctuating_h = False

# Running the model, please set variables in Constants.py
Global_act, Branching_global, Autocorrelation, Average_Activity, Average_Alpha, Avalanche_Distribution = BurnIn.Run_Model(cons.model, cons.N, cons.Seconds, h=cons.h, compiled=cons.compiled)



# getting the title h and the plotting color 
if cons.h == 10:
    title_h = r'$10^1$'
    color = '#FF1493'
if cons.h == 1:
    title_h = r'$10^0$'
    color = "green"
elif cons.h == 0.1:
    title_h = r'$10^{-1}$'
    color = '#BFA004'
elif cons.h == 0.01:
    title_h = r'$10^{-2}$'
    color = '#CB7600'
elif cons.h == 0.001:
    title_h = r'$10^{-3}$'
    color = "#BF0404"
elif cons.h == 0.0001:
    title_h = r'$10^{-4}$'
    color = "#8404D9"
elif cons.h == 0.00001:
    title_h = r'$10^{-5}$'
    color = "blue"
else:
    title_h = r'$10^{-6}$'
    color = "brown"



# Save some data from the run in the Runtime_Data folder
rd.save_run_data(Global_act, Branching_global, Autocorrelation, Average_Activity, Average_Alpha, Avalanche_Distribution)

# Print some statistics at the end
print("")
print("Used Modell: ", cons.model)
print("Number of Neurons: ", cons.N)
print("Running Time: ", cons.Seconds)
print("Input rate h:", cons.h)
print("Target Spiking Rate: ", cons.r_target)
print("Homeostatic Constant: ", cons.tau_hp)
print("Alpha init: ", cons.Alpha_init)
