import numpy as np
import Functions_Constants_Meters.Constants as cons

def External_Input_Subset(N: int, state_value: list, h: float, delta_t=cons.delta_t):
    # probability for external spike to activate Neuron 
    # I devide N by Subsetsize and multiply h by that amount so we get similar global stimulation
    h_sub = h*(N/cons.Subset_size)
    p = 1 - np.exp(-h_sub * delta_t)


    # calculate Bernulli, number of trials per Bernouli experiment is 1, as only one external Input (represents summed input)
    Activations = np.random.binomial(1, p, size=cons.Subset_size)

    # actualize the State_variable
    for i in range(cons.Subset_size):
        if Activations[i] == 1:
            state_value.append(i)


    return state_value

