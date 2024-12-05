import RESEARCH_Subset.Run_Model_Subset as Run_Model_Subset
import RESEARCH_Subset.ActivityPlot_Subset as act_plot
import RESEARCH_Subset.Homeostatic_plot_sub as homeo_plot
from Functions_Constants_Meters import Constants as cons
import Runtime_Data.Make_RuntimeData as rd
import time
# if its tests, cons.Subset should be True, fluctuating h false
cons.Subset = True
cons.Fluctuating_h = False
t1 = time.time()
# Running the model, please set variables in Constants.py
Global_act, Branching_global, Autocorrelation, Average_Activity_sub, Average_Activity_rest, Average_Alpha_sub, Average_Alpha_rest, Avalanche_Distribution, Time_Distribution, Avalanche_Distribution_sub, Avalanche_Distribution_rest, branch_sub, branch_rest = Run_Model_Subset.Run_Model_subset(cons.model, cons.N, cons.Seconds, cons.h, cons.compiled)
t2 = time.time()
print("Es hat ", int(t2-t1) ," Sekunden gebraucht")


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
rd.save_run_data_subset(Global_act, Branching_global, Autocorrelation, Average_Activity_sub, Average_Activity_rest, Average_Alpha_sub, Average_Alpha_rest, Avalanche_Distribution, Time_Distribution, Avalanche_Distribution_sub, Avalanche_Distribution_rest, branch_sub, branch_rest)

# Print some statistics at the end
print("")
print("Used Modell: ", cons.model)
print("Number of Neurons: ", cons.N)
print("Running Time: ", cons.Seconds)
print("Time Step Size: ", cons.delta_t)
print("Input rate h:", cons.h)
print("Target Spiking Rate: ", cons.r_target)
print("Homeostatic Constant: ", cons.tau_hp)
#print("last branching parameter: ", Branching_global[-1])
#print("last autocorrelation time: ", Autocorrelation[-1])
#print("Average_Alpha:", np.average(Alpha))
#plot.create_activityplot(Branching_global, "Branching Parameter every 100 Milliseconds", "green")
#plot.create_activityplot(Average_Alpha, "Mean homeostatic value", "green")
#plot.create_activityplot(Autocorrelation, "Autocorrelation", "green")
