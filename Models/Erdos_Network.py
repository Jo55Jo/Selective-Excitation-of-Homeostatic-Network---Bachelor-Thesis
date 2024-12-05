import numpy as np
import os
import sys
# append parent directory for importing constants
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
current_directory = os.getcwd()
from Functions_Constants_Meters import Constants as cons

# int, float -> np.ndarray of lists 
# Creates a N list of lists with a probability p for connection
def Erdos_Network(N: int, p = cons.pcon):
    Connection_arr = [list() for _ in range(N)]
    
    # Iterate through the whole Matrix
    for i in range(N):
        for j in range(N):
            # Do not draw self connections
            if i != j:
                # Making a Connection with probability p
                if np.random.rand() < p:  # compare random value with p
                    Connection_arr[i].append(j)
                    
    # Converting from array of lists to array of arrays 
    Connection_arr = [np.array(sublist) for sublist in Connection_arr]

    return Connection_arr

def Erdos_Inhomogen(N:int, s1:int, p1_internal: float, p1_external: float, p2_internal: float, p2_external: float):
    Connection_arr = [list() for _ in range(N)]
    
    # For the first half (internal connections)
    for i in range(s1):
        for j in range(s1):
            if i != j:
                if np.random.rand() < p1_internal:  # compare random value with p
                    Connection_arr[i].append(j)

    # First half to second half (external connections)
    for i in range(s1):
        for j in range(s1, N):
            if i != j:
                if np.random.rand() < p1_external:  # compare random value with p
                    Connection_arr[i].append(j)

    # For the second half (internal connections)
    for i in range(s1, N):
        for j in range(s1, N):
            if i != j:
                if np.random.rand() < p2_internal:  # compare random value with p
                    Connection_arr[i].append(j)

    # Second half to first half (external connections)
    for i in range(s1, N):
        for j in range(s1):
            if i != j:
                if np.random.rand() < p2_external:  # compare random value with p
                    Connection_arr[i].append(j)
                    
    # Converting from array of lists to array of arrays 
    Connection_arr = [np.array(sublist) for sublist in Connection_arr]

    return Connection_arr

# The Erdos_Mountain creates a Network that connects the Neurons in a Fixed way were the average connectivity is Fixed but disributed across neurons
# in a linear way from low to high connections
def Erdos_Mountain(N: cons.N, k=cons.Fixed):
    # calculate steps 
    steps = int(N/(k*2))+1
    connections = 1

    Connection_arr = [list() for _ in range(N)]
    
    # Iterate through the whole Matrix
    for i in range(N):
            if (i != 0) and i % steps == 0:
                connections += 1
            Connection_arr[i] = np.random.choice([x for x in range(N) if x != i], size=connections, replace=False).tolist()
    return Connection_arr


import pickle
import os
import numpy as np

def Erdos_Compiled(N, compiled):
    # Relativer Pfad zur Pickle-Datei
    relative_path = current_directory + r'/Models/Compiled_Models_SC/SC_' + str(compiled) + '.pkl'
    # Absoluter Pfad zur Pickle-Datei relativ zu der aktuellen Datei
    absolute_path = os.path.join(os.path.dirname(__file__), relative_path)

    # Lade die Pickle-Datei
    with open(absolute_path, 'rb') as file:
        Connection_Arr, Somata, Axons = pickle.load(file)

    # Länge der Verbindungen pro Axon
    len_con = [len(i) for i in Connection_Arr]
    array_of_lists = []

    for i in range(N):
        sublist_length = len_con[i]

        # Erstelle eine Liste von Indizes ohne `i`
        possible_indices = list(range(N))
        possible_indices.remove(i)  # Entferne `i`

        # Wähle sublist_length Indizes aus possible_indices ohne Wiederholung
        sublist = np.random.choice(possible_indices, size=sublist_length, replace=False).tolist()
        array_of_lists.append(sublist)

    return array_of_lists
