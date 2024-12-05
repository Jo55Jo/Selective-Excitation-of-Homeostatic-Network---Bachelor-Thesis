import numpy as np
#import Functions_Constants_Meters.Constants as cons

#----------------------------------------
# Necessary Constants
#Timestep = cons.delta_t
#----------------------------------------

# int, ndarray -> ndarray (updated state_values)
# Sets the State_value to active with a certain probability that depends on the external-input-rate h and the timeconstant tau
def External_Input(N: int, state_value: list, h: float, delta_t):
    # probability for external spike to activate Neuron
    p = 1 - np.exp(-h * delta_t)

    # calculate Bernulli, number of trials per Bernouli experiment is 1, as only one external Input (represents summed input)
    Activations = np.random.binomial(1, p, size=N)

    new_state_value = state_value.copy()  # or initialize as an empty list

    # actualize the State_variable
    for i in range(N):
        if Activations[i] == 1:
            new_state_value.append(i)

    return new_state_value




# Takes the Neuron array of array, the homeostatic-scaling-array, the old state-value-array, the actual state-value-array calculates the update of the state-value array
#! Because it is very unlikely that an neuron was activated by external input, we first calculate whether it is updated by previous activation and then check whether it is already active
def Spike_Propagation(Connection_arr: np.ndarray, state_value_new: list, state_value_old: list, Alpha: np.ndarray):
    #The new state_value includes the externaly activated neurons

    # for every neuron that was active last iteration
    for neuron in state_value_old:
        neuron = int(neuron)

        # for every connection with a neuron that was active in t_-1
        for con_neuron in Connection_arr[neuron]:
            con_neuron = int(con_neuron)
    
        # Calculate the probability for Neuron i to be Active with homeostatic scaling factor of i and number of activated connections
            if np.random.binomial(1, Alpha[con_neuron]) == 1:

                #check whether the neuron is already activ
                if con_neuron not in state_value_new:
                    state_value_new.append(con_neuron)

    return state_value_new


#ndarray, ndarray -> nd.array (update of homeostatic-scaling-values)
#takes the array of state-value and homeostatic-scaling-factor and returns the updated homeostatic-scaling-factor
def Update_Alpha(state_value: list, Alpha: np.ndarray, tau_hp, delta_t, log_r, log_target, r_target):
    # For every neuron ist homeostatic-scaling-factor is adjusted
    for i, Alpha_i in enumerate(Alpha):
        #calculate Delta_Alpha[i]
        if i in state_value:
            Alpha_updated = Alpha_i + Delta_Alpha(1, i, tau_hp, delta_t, log_r, log_target, r_target)
        else:
            Alpha_updated = Alpha_i + Delta_Alpha(0, i, tau_hp, delta_t, log_r, log_target, r_target)

        #update Apha[i]
        Alpha[i] = Alpha_updated
    
    #! Alpha cannot be bigger then 1, can it? No, as it will create the probability for an activation which therefor has to be between 0/1
    Alpha = np.clip(Alpha, 0, 1)

    return Alpha



#int (0 or 1) -> float
#takes statevalue for individual neuron and returns the update value for homeostatic scaling factor
#int (0 or 1) -> float
#takes statevalue for individual neuron and returns the update value for homeostatic scaling factor

def Delta_Alpha(state_value: int, neuron: int, tau_hp, delta_t, log_r, log_target, r_target):
    if not log_r:
        alpha = (delta_t*r_target-state_value)*(delta_t/tau_hp)
    else:
        alpha = (delta_t*log_target[neuron]-state_value)*(delta_t/tau_hp)
    return alpha
