import numpy as np
#import math
from Functions_Constants_Meters import Constants as cons


#! Not used anymore because it makes more sense to do it directly during runtime
'''
# np.ndarray -> int
# counts how many Neurons are activ at a given time
def Global_Activity(state_value_new: list):
    A = len(state_value_new)
    return A

#! Das ist irgendwie komisch gemacht. Das ergibt glaube ich wenig Sinn
# int(global activity), int(momentan iteration (seconds/delta_t)), int(average_constant), float (delta_t) -> float(average_activity)
# returns the average activity for every "average_constant" iteration (every delta_t)
def Average_Activity(N: int, glob: int, iteration: int, average_constant = 4, delta_t = cons.delta_t):

    if iteration % 4 == 0:
        #The paper uses Delta_t = 4 Millisekonds so 4 times deltat
        average_activity = glob/N*delta_t*4
    return average_activity
'''
        

    


# np.ndarray (matrix), list (state_values) --> int (global branching parameter), np.array of ints (individual branching parameter)
# calculates the branching parameters.
def Branching_Parameters(N: int, Connection_arr: np.ndarray, Alpha: np.array, model, k):
    # Initialize array of individual branching_parameters. It has the same size as state_value_new.
    Branching_Parameter_ind = np.zeros(N)
    
    if model == "AA":
        Branching_Parameter_ind = Alpha * k
    else:
        Connection_lengths = [len(i) for i in Connection_arr]
        Branching_Parameter_ind = Alpha * Connection_lengths
    # calculate the global_branching_parameter
    if cons.Subset:
        Branching_Parameter_sub = Branching_Parameter_ind[0:cons.Subset_size].mean()
        Branching_Parameter_rest = Branching_Parameter_ind[cons.Subset_size:].mean()
    Branching_Parameter_global = Branching_Parameter_ind.mean()
    
    if cons.Subset:
        return Branching_Parameter_global, Branching_Parameter_sub, Branching_Parameter_rest
    else:
        return Branching_Parameter_global


# float (Timeconstant), float (Branching_Parameter_gloabal) --> float (Autocorrelation_time)
# calculates Autocorrelation time
def Autocorrelation_Time(del_t: float, Branch_glob: float):
    if Branch_glob == 0:
        return 0
    else:
        tau = del_t/np.log(Branch_glob)

    return tau

