import sqlite3
import numpy as np
import json
import pickle

from Models import Spacial_Clustered as SC

# connect to databank
conn = sqlite3.connect('Models/Compiled_Models/SC_compiled.db')
cursor = conn.cursor()

# Tabelle erstellen, falls sie noch nicht existiert
cursor.execute('''CREATE TABLE IF NOT EXISTS Spacial_Clustered_10000
                  (array_key TEXT PRIMARY KEY, array_json TEXT)''')

# getting number of elements in the table
'''cursor.execute("SELECT COUNT(*) FROM Spacial_Clustered_10000")
row_count = cursor.fetchone()[0]
print("Anzahl der Elemente in der Datenbank:", row_count)
'''


# the array name to be joined:
for i in range(9):
    SC_name = "SC_10000_" + str(i+1)
    #Spacial_clust = SC.Spacial_Clustered(10000)

    array_pickle = pickle.dumps(Spacial_clust)

    # write new data into the table
    cursor.execute("INSERT INTO Spacial_Clustered_10000 (array_key, array_json) VALUES (?, ?)",
               (SC_name, array_pickle))
    conn.commit()
    print(i)

# close connection
conn.close()

