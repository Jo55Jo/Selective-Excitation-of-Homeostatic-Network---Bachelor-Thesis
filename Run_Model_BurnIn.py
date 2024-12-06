import numpy as np
import math
from Models import Annealed_Average as AA
from Models import Erdos_Network as ER
from Models import Spacial_Clustered as SC
from Functions_Constants_Meters import Functions as funs
from Functions_Constants_Meters import Constants as cons
from Functions_Constants_Meters import Meters as meters
import sqlite3
import time
import pickle
import os
import sys
# append parent directory for importing constants
current_directory = os.getcwd()


# String (modell), int (size), int(iterations), float (input is one of: [0, 0.1, 0.01, 0.001, 0.0001]) -> , list (Population activity), list of np.ndarrays (individual activity), list (Branching Paramete$
# model is one of: "AA", "ER", "SC", "SC_10000_{i}"
# all meters are set to true by default. 
# Population_activity --> int; returns the global activity
# Branching_Parameters --> np.ndarray, int; returns list of individual branchingP  and int = global_mean_of_branchingP
# Autocorrelation_tiem --> int; returns int giving the autocorrelation time
# runs the whole model. Individual Parameters for models or functions have to be adjusted in the according files

def Run_Model(model: str, N: int, Seconds: int, h: float, compiled):
    # initialize state_value_old, Alphaa (homostatic array)
    state_value_old = []
    # initializing Alpha. As k = 4 in the models we use 0.25 for h≠1 (h=1 we use 0 so that it doesnt take so long until its giving resonable results)
    Alpha           = np.random.normal(cons.Alpha_init, cons.SD_init, N)
    # Alpha           = np.zeros(N)
    # Calculate Iterations given by Seconds/delta_t, cast to int with math.ceil
    Iterations = math.ceil(Seconds/cons.delta_t)

    # Initialize lists for meters
    Global_act = []
    Branching_global = []
    Autocorrelation = []
    Average_Activity = []
    Average_Alpha = []

    #Initializing
    state_value_new = np.random.choice(N, size=cons.Init_Activity, replace=False).tolist()


    #Avalanche distribution tracker initialized as 0 and updated once activity ≠ 0
    Avalanche_Tracker = 0
    Avalanche_Distribution = []

    #Activity Tracker for measuring average activity
    Activity_Tracker = 0

    # for "AA", the connarr must be created before 
    if model == "AA":
        # create an array of N empty lists
        Connection_arr = [[] for _ in range(N)]


    for i in range(Iterations):
        if i<=100000:
            tau_hp=1
        if 100000<i<=300000:
            tau_hp=10
        if 300000<i<=cons.Burn_In:
            tau_hp=100
        if i>=cons.Burn_In*1000:
            tau_hp=cons.tau_hp
        # get Connection Array
        # if it is the first iteration or AA is chosen we draw the Connection_arr
        if (model == "SC_Compiled") and (i == 0):
            file_path = os.path.join(current_directory, 'Models', 'Compiled_Models_SC', f'SC_{compiled}.pkl')
            with open(file_path, 'rb') as file:
                Connection_arr, Somata, Axons  = pickle.load(file)
        if (model != "AA") and (model != "SC_Compiled") and (model != "ER_Fixed") and  (i == 0): 
            Connection_arr = Get_connection_array(N, model)
        if (model == "ER_Fixed") and (i == 0):
            Connection_arr = np.array([np.random.choice([x for x in range(N) if x != i], size=cons.Fixed, replace=False).tolist() for i in range(N)])


        # nacheinander Funktionen ausführen
        external_activated = funs.External_Input(N, state_value_new, h, cons.delta_t)
        state_value_new = funs.Spike_Propagation(Connection_arr, external_activated, state_value_old, Alpha)
        Alpha = funs.Update_Alpha(state_value_new, Alpha, tau_hp, cons.delta_t, cons.log_r, cons.log_target, cons.r_target)

        # meter global and global average activity 
        glob_t = len(state_value_new)
        Activity_Tracker += glob_t

        
        # we calculate the average global activity for time steps of 4 Milliseconds
        if (i % 4 == 0) and (i>=cons.Burn_In*1000):
            #Update average Activity and average Alpha
            Average_Activity_t = Activity_Tracker / (N * cons.delta_t_act)
            average_alpha_t = np.average(Alpha)

            # Reset the activity tracker to 0
            Activity_Tracker = 0

            # append every 4 Seconds to the lists for average Activity and average alpha
            Average_Activity.append(Average_Activity_t)
            Average_Alpha.append(average_alpha_t)


        #Do metering of Branching parameter and autocorrelation
        if (i % 100 == 0) and (i>=cons.Burn_In*1000):

            branch_glob = meters.Branching_Parameters(N, Connection_arr, Alpha, model, cons.k)
            autocorr_t = meters.Autocorrelation_Time(cons.delta_t, branch_glob)

            # add meters to collection
            Branching_global.append(branch_glob)
            Autocorrelation.append(autocorr_t)


        # If there is zero activity but the tracker is not 0, then the avalanche is over so return to 0 and 
        if i>=cons.Burn_In*1000:
            if (glob_t == 0) and (Avalanche_Tracker != 0):
                Avalanche_Distribution.append(Avalanche_Tracker)
                Avalanche_Tracker = 0
            if glob_t != 0:
                Avalanche_Tracker += glob_t


        if model == "AA":
            if cons.Homo:
                Connection_arr = [[] for _ in range(N)]
                for neuron in state_value_new:
                    if (neuron >= N-cons.Homo_Size) and not(neuron == N-1):
                        connections = [i for i in range(N-cons.Homo_Size, N-1)]
                    elif (neuron == N-1):
                        connections = [i for i in range(N-1)]
                    elif neuron == N-cons.Homo_Size-1:
                        connections = np.random.choice(N-cons.Homo_Size, size=cons.k, replace=False)
                    else:
                        connections = np.random.choice(N-1, size=cons.k, replace=False)
                    connections.sort()
                    Connection_arr[neuron].extend(connections) 
                if i % 100000 == 0:
                    individual_branch = Alpha[:-1]*cons.k
                    individual_branch.append(N-1*Alpha[-1])
                    # Füge die individuellen Verzweigungsparameter zur globalen Aktivität hinzu
                    Global_act.append(individual_branch)
            else: 
                # first the Connection_array has to be set to zero
                # create an array of N empty lists
                Connection_arr = [[] for _ in range(N)]
                for neuron in state_value_new:
                    connections = np.random.choice(N, size=cons.k, replace=False)
                    connections.sort()
                    Connection_arr[neuron].extend(connections)
                if (i % 100000 == 0):
                    len_con = [len(i) for i in Connection_arr]
                    individual_branch = Alpha*len_con
                    Global_act.append(individual_branch)


        if (i % 100000 == 0) and (model != "AA"):
            len_con = [len(i) for i in Connection_arr]
            individual_branch = Alpha*len_con
            Global_act.append(individual_branch)
        if (i % 1000 == 0):
            print(str(i/1000) + " Seconds of " + str(Seconds))
            

        # state_value_new becomes the new state_value_old
        state_value_old = state_value_new
        state_value_new = []

    return Global_act, Branching_global, Autocorrelation, Average_Activity, Average_Alpha, Avalanche_Distribution

# string -> array of lists
# Choice is one of ["AA", "ER", "SC", "SC_10000_{i}"] <- "SC_10000_{i}" takes an already compiled Conn_array from a database where i is the specific array. 

def Get_connection_array(N, model: str):
    if model == "ER":
        Connection_array = ER.Erdos_Network(N)
#    elif model == "ER_POP":
#        Connection_array = ER.Erdos_Inhomogen(N, cons.s1, cons.p1i, cons.p1e, cons.p2i, cons.p2e)
    elif model == "SC":
        Connection_array = SC.Spacial_Clustered(N)
    elif model == "HM":
        Connection_array = HM.HierarchicalModel(cons.level)
    elif model == "ER_Mountain":
        Connection_array = ER.Erdos_Mountain(cons.N, cons.Fixed)
    elif model == "Erdos_Compiled":
        Connection_array = ER.Erdos_Compiled(N, cons.compiled)

    return Connection_array




