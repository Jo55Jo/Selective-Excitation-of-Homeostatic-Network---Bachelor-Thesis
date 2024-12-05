import numpy as np
import math
import sys
import os
# append parent directory for importing constants
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
from Functions_Constants_Meters import Constants as cons

#! Scaling field size depending on number of neurons
FIELD_SIZE = int(5000*math.sqrt(cons.N/10000))

# int (N), int (dentritic radii = 20müm in paper == 20) -> NxN matrix (connections)
# X_sorted list of somata, the list of axons, the dentritic radii and the number of neurons are given into the Function that draws the connections into the connection matrix. 


def Spacial_Clustered(N: int, dentritic_radius = 20):
    # initialize the connection array with empty lists
    Connection_arr = [list() for _ in range(N)]

    # Create list of Somatas (list of touples)
    Somata = []
    Somata = Draw_Somata(N, Somata)

    # Create list of Axons (list of list of touples)
    Axons = Draw_Axons(N, Somata)

    # for every neuron
    for i in range(len(Axons)):
        #for every segment in that Neuron
        for j in range(len(Axons[i])-1):
            # calculate the bigger and smaller x-coordinate. We do it in the i'th list of segments and for the j'ths segment. 
            if Axons[i][j][0] >= Axons[i][j+1][0]:
                # Segment_1 is the segment with the bigger x component.
                Segment_1 = Axons[i][j]
                Segment_0 = Axons[i][j+1]
            else:
                Segment_1 = Axons[i][j+1]
                Segment_0 = Axons[i][j]

            # define the boundaries in which we will look for intersections
            lower_bound = Segment_0[0] - dentritic_radius
            upper_bound = Segment_1[0] + dentritic_radius

            # for every soma that is in x-range, so that we do not have to calculate it with every Soma.
            for k, Soma in enumerate(Somata):
                # if somata already in the list:
                if k in Connection_arr[i]:
                    continue

                # if the somas x_coordinate is bigger then the upper bound then the intersection is impolible and we can continue with the next segment
                if Soma[0] > upper_bound:
                    continue

                # if it is in range, and it is intersecting, and it is not a self connection
                if Soma[0] > lower_bound:
                    if (is_intersecting(Segment_0, Segment_1, Soma, dentritic_radius) == True) and not(k == i):
                        Connection_arr[i].append(k)
    
    #Converting from array of lists to array of arrays 
    Connection_arr = [np.array(sublist) for sublist in Connection_arr]
    return Connection_arr, Somata, Axons



# int, float, float -> 1 x list of tuples (ordered in x direction)
# takes number of neurons,  field_size and soma-radus and returns 2 lists...
# ...of touples (points), ordered in x direction
#! Neurons are spawned on Integer Grid.
#! I start the Somas at 20 and stop at 4980 so that they don't go over the boundary
def Draw_Somata(N: int, Somata = [], field_s = FIELD_SIZE, Soma_r = 7.5, dentritic_r = 20):

    #redo it recursively for every time it failed because radii overlaped
    fails = 0
    for Neuron in range(N):
        # Field with border of size dentritic-radius
        x = np.random.randint(dentritic_r, field_s-dentritic_r)
        y = np.random.randint(dentritic_r, field_s-dentritic_r)

        # if its the first Neuron just put it in the list
        if  Somata == []:
            Somata.append((x,y))
            continue


        # iterate through Somata and compare x and y with all those who are in range of x
        Somata_length = len(Somata)
        for i in range(Somata_length):
            # if Somata[i] in list is further away in x direction, we can draw Soma
            if Somata[i][0] > x+Soma_r:
                Somata.insert(i, (x, y)) 
                break

            # if it is in range, also check for y and if y is also in range, then there is a fail, otherwise draw neuron
            if Somata[i][0] > x-Soma_r:
                if Somata[i][1] > y-Soma_r and Somata[i][1] < y+Soma_r:
                    fails += 1
                    break
            else:
                Somata.insert(i, (x, y))
                break
    if fails > 0:
        Draw_Somata(fails, Somata)

    # if we have the subset condition, We want to plot the inner neurons red so we sort the array such that most central neurons are at the beginning
    if cons.Subset:
        Somata = sort_by_distance(Somata, FIELD_SIZE)

    return Somata




# list -> list of lists 

# Average length of axon = 1.1mm
# Standard deviation of lenght = 900mum
# Segment length = 10mum (semiflexibel axon growth)
# Orientation drawn from gaussian distribution with sigma = 15° and average = 0.

# Takes the x_sorted somata list and outputs an list of list. each sublist is a axon with segments. Each Point
# between which the segments are, is one entrie in the list, starting with the somata. 
# The list is sorted in the same order as the somata List. 
def Draw_Axons(N:int , Somata: list, field_s = FIELD_SIZE, axon_length_average = 1100, rayleigh_scale = 0.9, segment_length = 10, sigma_angle = 15):
    #initialize the list of axons
    Axons = np.empty(N, dtype=object)
    Axons[:] = [list() for _ in range(N)]

    # initialize array of axon lenghts drawn from rayligh distribuition #! made by chatGPT (just using np.random.rayleigh doesnt work)
    axon_lengths = np.random.rayleigh(rayleigh_scale, N)
    #! ChatGPT made funny stuff. Now it should fit. First i draw from Rayleigh with scale of 0.9 and then multiply by average length
    # Die mittlere Länge nach dem Skalieren auf 1100 korrigieren
    scale_factor = axon_length_average / np.mean(axon_lengths)
    axon_lengths_scaled = axon_lengths * scale_factor

    
    #for every neuron in x_sorted
    for i, Soma in enumerate(Somata):
        # draw the Somas position at the first entrie of its axons list by first adding the list and then adding the Neuron to that list
        Axons[i].append(Soma)

        # get x and y of Neuron 
        Neuron_x = Soma[0]
        Neuron_y = Soma[1]

        # use the previous orientation angle to calculate the next axon segment
        pre_orientation_angle = 0

        # index for tracking segment
        index = 0

        # get the i'ths axon length
        axon_length_i = axon_lengths_scaled[i]

        while axon_length_i > 0:
            # if rest of axon_length is smaler then the segment lengt, then the segment length is the rest of the axons length
            if axon_length_i >= segment_length:
                segment_length_i = segment_length
            else:
                segment_length_i = axon_length_i

            #caluculate the next point of the axon. the orientation is random from 360 if its the first neuron. After that its drawn from a gaussian.
            if index == 0:
                # draw Orientation randomly from 0-360 degrees with floats
                orientation_angle = np.random.uniform(0, 360)
            else: 
                # draw orientation from normal distribuition with mean of last angle and given deviation (paper = 15°)
                orientation_angle = np.random.normal(pre_orientation_angle, sigma_angle)
            
            # calculate new point. Neuron_x and Neuron_y are now the points of the last points of the drawn axon
            Neuron_x, Neuron_y = new_point_from_angle_distance(Neuron_x, Neuron_y, orientation_angle, segment_length_i)
            
            #create no boundary field
            if Neuron_x > field_s:
                Neuron_x = Neuron_x-field_s
            if Neuron_x < 0: 
                Neuron_x = Neuron_x+field_s
            if Neuron_y > field_s:
               Neuron_y = Neuron_y-field_s
            if Neuron_y < 0: 
                Neuron_y = Neuron_y+field_s
            
            # add the new point to the axons list.
            Axons[i].append((Neuron_x, Neuron_y))

            # calculate the remaining length of the axon, increment index so its clear whether its the first segment or not
            axon_length_i -= segment_length_i
            index +=1
            pre_orientation_angle = orientation_angle

    return Axons







# --------------------- Helper Functions -----------------

# ---> Helperfunction for Draw_Axons 
# float, float, float, float -> float, float
# Takes the point, the angle of orientation and the distance and calculates where the next point of the segment has to be
def new_point_from_angle_distance(x1, y1, angle_degrees, distance):
    # Convert angle from degrees to radians
    angle_radians = math.radians(angle_degrees)
    
    # Calculate change in x and y coordinates
    delta_x = distance * math.cos(angle_radians)
    delta_y = distance * math.sin(angle_radians)
    
    # Calculate new coordinates
    x2 = x1 + delta_x
    y2 = y1 + delta_y
    
    return x2, y2


# tupel, tupel, tupel, int -> boolean
# checks whether a dentritic tree of a soma is intersectig with a axonal segment (Strecke mit Kreis)
# it does this in three steps:
# 1. check whether soma is in range of a end point of the segment.
# 2. Check whether it is outside of 2 lines drawn verticali to the segment between the two points.
# 3. Check whether it is intersecting with the line defined by the two points. 
def is_intersecting(point1, point2, soma, radius):
    # if it is in range of the endpoints of the segment then it is intersecting
    if (is_inrange(point1, soma, radius) or is_inrange(point2, soma, radius)) == True:
        return True
    else:
        # if it is not intersecting with the endpoints and is not inside the horizontal lines from the Endpoints it is not intersecting
        if is_inside_horizontal_lines(point1, point2, soma) == False:
            return False
        else:
            # if it is not intersecting with the endpoints and is not inside the horizontal lines and is not in range of the line then it is not intersecting. Otherwise it is intersecting
            if does_line_intersect_circle(point1, point2, soma, radius) == True:
                return True
            else:
                return False




# --------------------- Helper-Helper Functions --------------------

# ---> 1. Helper-helperfunction for is_intersecting
# tupel, tupel, int -> boolean
# check whether a point is in range of another point
def is_inrange(point1, point2, radius):
    distance = np.linalg.norm(np.array(point2) - np.array(point1))
    
    if distance <= radius:
        return True
    else:
        return False

# ---> 2. Helper-helperfunction for is_intersecting
# tupel, tupel, tupel, int --> boolean
# Check whether it is outside of 2 lines drawn verticali to the segment between the two points.
def is_inside_horizontal_lines(point1, point2, soma):

    # point1-point2 vector.
    vec_point1_point2 = np.array(point2) - np.array(point1)

    # calculate the vertical vector to the point1, point2 vector.
    vec_point1_point2_horizontal = -vec_point1_point2
    
    # Checking the bend of the horizontal vector. If the absolut x component is bigger then the absolut y component then we norm to y. Otherwise to x.
    if abs(vec_point1_point2_horizontal[0]) <= abs(vec_point1_point2_horizontal[1]):
        # norm the vector in y-direction, this implies that the y component is +1
        vec_point1_point2_horizontal_ynorm = vec_point1_point2_horizontal/vec_point1_point2_horizontal[1]

        # calculate the distance of soma to point1,2 in y direction. We need to know whether the line is growing or faling to know whether to add or subtract the vector
        # case when vec_point1_point2_horizontal_norm is growing
        if vec_point1_point2_horizontal_ynorm[0] <= 0:
            dist1_y = soma[1] - point1[1]
            dist2_y = soma[1] - point2[1]

        # case when vec_point1_point2_horizontal_norm is falling
        else:
            dist1_y = point1[1] - soma[1] 
            dist2_y = point2[1] - soma[1] 

        # calculate the x-coordinate where the horizontal line running through "soma" is cutting the vertical lines through the endpoints of the segment
        point1_new = point1 + vec_point1_point2_horizontal_ynorm * dist1_y
        point2_new = point2 + vec_point1_point2_horizontal_ynorm * dist2_y

        # if soma_x is in between the two intersection points, so inbetween the x coordinates of point1_new and point2_new, then it is in between the lines. Otherwise it is outside
        if (point1_new[0] < soma[0] < point2_new[0]) or (point1_new[0] > soma[0] > point2_new[0]):
            return True
        else:
            return False
    
    
    # if abs(x) > abs(y), do it for x
    else:
        # norm the vector in y-direction, this implies that the y component is +1
        vec_point1_point2_horizontal_xnorm = vec_point1_point2_horizontal/vec_point1_point2_horizontal[0]

        # calculate the distance of soma to point1,2 in x direction. We need to know whether the line is growing or faling to know whether to add or subtract the vector
        # case when vec_point1_point2_horizontal_norm is growing
        if vec_point1_point2_horizontal_xnorm[0] >= 0:
            dist1_x = soma[0] - point1[0]
            dist2_x = soma[0] - point2[0]
        # case when vec_point1_point2_horizontal_norm is falling
        else:
            dist1_x = point1[0] - soma[0] 
            dist2_x = point2[0] - soma[0] 

        # calculate the x-coordinate where the horizontal line running through "soma" is cutting the vertical lines through the endpoints of the segment
        point1_new = point1 + vec_point1_point2_horizontal_xnorm * dist1_x
        point2_new = point2 + vec_point1_point2_horizontal_xnorm * dist2_x

        # if soma_x is in between the two intersection points, so inbetween the x coordinates of point1_new and point2_new, then it is in between the lines. Otherwise it is outside
        if (point1_new[1] < soma[1] < point2_new[1]) or (point1_new[1] > soma[1] > point2_new[1]):
            return True
        else:
            return False
        



# ---> 3. Helper-helperfunction for is_intersecting
# tupel, tupel, tupel, int -> boolean
# check whether a circle (dentritic tree) is intersecting with an line
def does_line_intersect_circle(point1, point2, soma, radius):
    
    # calculate vectors between point 1,2 and 1,center
    vec_p12 = np.array(point2) - np.array(point1)
    vec_p1center = np.array(soma) - np.array(point1)


    # norm and vectornorm of vec_p12
    vec_p12_norm = np.linalg.norm(vec_p12)
    vec_p12_vnorm = vec_p12 / vec_p12_norm


    # calculate the projection
    projection_length = np.dot(vec_p1center, vec_p12) / vec_p12_norm


    # calculate the clostest point to the line
    closest_point_on_line = point1 + vec_p12_vnorm  * projection_length

    # calculate the vector between those points
    vec_center_to_closest_point = np.array(soma) - np.array(closest_point_on_line)
    
    # calculate distance to line 
    distance_to_line = np.linalg.norm(vec_center_to_closest_point)
    
    # check whether the distance of soma to axon is bigger then dentritic tree
    if distance_to_line <= radius:
        return True
    else:
        return False


#--------------------------- helper for somata in subset condition (made by Gpt) ---------------------------
def distance_from_center(point, center):
    """
    Calculate the Euclidean distance between a point and the center.
    """
    return math.sqrt((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2)

def sort_by_distance(coords, field_size):
    """
    Sorts a list of tuples (coordinates) by their distance from the center of the field.
    
    Args:
    - coords: List of tuples representing coordinates (x, y).
    - field_size: Size of the field (assuming square field of field_size x field_size).
    
    Returns:
    - List of tuples sorted by distance from the center.
    """
    center = (field_size / 2, field_size / 2)
    sorted_coords = sorted(coords, key=lambda point: distance_from_center(point, center))
    return sorted_coords


#--------------------------- tests ---------------------------
def run_tests_is_intersecting():
    # Test 1: Linie schneidet den Kreis
    assert is_intersecting((0, 0), (5, 5), (3, 3), 2) == True, "Test 1"
    
    # Test 2: Linie schneidet den Kreis nicht
    assert is_intersecting((0, 0), (1, 1), (2, 2), 2) == True, "Test 2"
    
    # Test 3: Linie ist ein Durchmesser des Kreises (berührt sich nur)
    assert is_intersecting((1, 1), (3, 3), (3, 3), 2) == True, "Test 3"
    
    # Test 4: Linie ist ein Radius des Kreises (berührt sich nur)
    assert is_intersecting((1, 1), (3, 3), (-1, 1), 2) == True, "Test 4"
    
    # Test 5: Linie ist innerhalb des Kreises
    assert is_intersecting((1, 1), (2, 2), (5, 5), 2) == False, "Test 5"
    
    # Test 6: Linie ist außerhalb des Kreises
    assert is_intersecting((10, 10), (15, 15), (10, 3), 2) == False, "Test 6"

    assert is_intersecting((10, 10), (15, 15), (3, 3), 2) == False, "Test 7"
    
    print("Alle Tests erfolgreich durchgeführt!")


# Testfälle ausführen
def run_tests_is_inside_horizontal_lines():
    # Testfall 1: Soma innerhalb der horizontalen Linien
    point1 = [0, 0]
    point2 = [2, 2]
    soma = [1, 1]
    assert is_inside_horizontal_lines(point1, point2, soma) == True, "Testfall 1 fehlgeschlagen"
    
    # Testfall 2: Soma außerhalb der horizontalen Linien
    point1 = [0, 0]
    point2 = [3, 3]
    soma = [5, 5]
    assert is_inside_horizontal_lines(point1, point2, soma) == False, "Testfall 2 fehlgeschlagen"
    
    # Testfall 3: Soma auf einer horizontalen Linie
    point1 = [0, 0]
    point2 = [3, 3]
    soma = [2, 2]
    assert is_inside_horizontal_lines(point1, point2, soma) == True, "Testfall 3 fehlgeschlagen"
    
    # Testfall 4: Soma auf einer vertikalen Linie
    point1 = [0, 0]
    point2 = [0, 3]
    soma = [0, 2]
    assert is_inside_horizontal_lines(point1, point2, soma) == False, "Testfall 4 fehlgeschlagen"

    print("Alle Testfälle erfolgreich ausgeführt.")


def run_tests_is_inrange():
    # Testfall 1: Punkte innerhalb des Radius
    point1 = [0, 0]
    point2 = [1, 1]
    radius = 2.0
    assert is_inrange(point1, point2, radius) == True, "Testfall 1 fehlgeschlagen"
    
    # Testfall 2: Punkte außerhalb des Radius
    point1 = [0, 0]
    point2 = [3, 3]
    radius = 2.0
    assert is_inrange(point1, point2, radius) == False, "Testfall 2 fehlgeschlagen"
    
    # Testfall 3: Punkte auf dem Radius
    point1 = [0, 0]
    point2 = [2, 2]
    radius = 2.0
    assert is_inrange(point1, point2, radius) == False, "Testfall 3 fehlgeschlagen"
    
    # Testfall 4: Radius ist null
    point1 = [0, 0]
    point2 = [1, 1]
    radius = 1.5
    assert is_inrange(point1, point2, radius) == True, "Testfall 4 fehlgeschlagen"

    print("Alle Testfälle erfolgreich ausgeführt.")

def run_tests_does_line_intersect_circle():
    # Testfall 1: Linie durch den Mittelpunkt des Kreises
    point1 = [0, 0]
    point2 = [2, 2]
    soma = [1, 1]
    radius = 1.0
    assert does_line_intersect_circle(point1, point2, soma, radius) == True, "Testfall 1 fehlgeschlagen"
    
    # Testfall 2: Linie nicht durch den Kreis
    point1 = [0, 0]
    point2 = [3, 3]
    soma = [5, 5]
    radius = 1.0
    assert does_line_intersect_circle(point1, point2, soma, radius) == True, "Testfall 2 fehlgeschlagen"
    
    # Testfall 3: Linie tangiert den Kreis
    point1 = [0, 0]
    point2 = [3, 3]
    soma = [2, 2]
    radius = 1.0
    assert does_line_intersect_circle(point1, point2, soma, radius) == True, "Testfall 3 fehlgeschlagen"
    
    # Testfall 4: Linie ist eine vertikale Linie
    point1 = [0, 0]
    point2 = [0, 3]
    soma = [1.1, 0]
    radius = 1.2
    assert does_line_intersect_circle(point1, point2, soma, radius) == True, "Testfall 4 fehlgeschlagen"

    # Testfall 5: Big numbers
    point1 = [0, 0]
    point2 = [0, 3]
    soma = [1.1, 0]
    radius = 1.2
    assert does_line_intersect_circle(point1, point2, soma, radius) == True, "Testfall 4 fehlgeschlagen"

    print("Alle Testfälle erfolgreich ausgeführt.")
'''
start_time = time.time()
print(start_time)
Connection_Arr, Somata, Axons = Spacial_Clustered(10000)

end_time = time.time()
total_time = end_time - start_time


print("Spacial Clustered Time: ", total_time)


'''
