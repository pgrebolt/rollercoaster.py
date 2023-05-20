# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 15:24:00 2023

@author: Pau Grèbol Tomàs
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.integrate as spint
from scipy.spatial.transform import Rotation as R
import pdb

#Carreguem les dades
file = 'IndianaJonesDisney071219.csv'
data = pd.read_csv(file, delimiter=',')
#Guardem les dades a les arrays corresponents
time, ax, ay, az, wx, wy, wz = data['time'].values, data['ax'].values, data['ay'].values,\
                                data['az'].values, data['wx'].values, data['wy'].values, data['wz'].values #Pot ser que els eixos els haguem de cnaviar

#L'array de temps té alguns valors que són duplicats. Per evitar problemes ens quedem amb un sol valor dels duplicats
def remove_duplicates_with_indices(arr):
    unique_indices = {}
    for i, val in enumerate(arr):
        if val not in unique_indices:
            unique_indices[val] = i
    return np.array(list(unique_indices.values()))
good_idxs = remove_duplicates_with_indices(time) #Ens treiem de sobre uns 400 punts dolents!

#Guardem les noves arrays
time, ax, ay, az, wx, wy, wz = time[good_idxs], ax[good_idxs], ay[good_idxs], az[good_idxs], wx[good_idxs], wy[good_idxs], wz[good_idxs]

#Calculem els passos de temps
tvar = [time[i]-time[i-1] for i in range(len(time))]
tvar[0] = 0. #Redefinim el punt inicial

#Si volem trobar l'angle respecte el sistema inicial a cada instant de temps
ox, oy, oz = np.zeros(len(time)), np.zeros(len(time)), np.zeros(len(time))
for i in range(len(time)):
    if i == 0:
        continue
    else:
        ox[i] = ox[i-1] + wx[i]*tvar[i] #Reescrivim un valor pel producte de les seves matrius de rotació
        oy[i] = oy[i - 1] + wy[i] * tvar[i]  # Reescrivim un valor pel producte de les seves matrius de rotació
        oz[i] = oz[i - 1] + wz[i] * tvar[i]  # Reescrivim un valor pel producte de les seves matrius de rotació
        if ox[i] > 2*np.pi:
            ox[i] = ox[i] - 2*np.pi
        elif ox[i] < 2*np.pi:
            ox[i] = ox[i] + 2*np.pi
        if oy[i] > 2*np.pi:
            oy[i] = oy[i] - 2*np.pi
        elif oy[i] < 2*np.pi:
            oy[i] = oy[i] + 2*np.pi
        if oz[i] > 2*np.pi:
            oz[i] = oz[i] - 2*np.pi
        elif oz[i] < 2*np.pi:
            oz[i] = oz[i] + 2*np.pi

#Matrius de rotació en cada eix
rx, ry, rz = R.from_euler('x', wx*tvar).as_matrix(), R.from_euler('y', wy*tvar).as_matrix(),\
            R.from_euler('z', wz*tvar).as_matrix()
#Aquests elements contenen les matrius de rotació que cal aplicar a cada punt, però les velocitats estan mesurades a partir de la posició
#anterior. Per trobar-ho respecte la posició inicial cal aplicar successives rotacions

for i in range(len(time)):
    if i == 0:
        continue
    else:
        rx[i] = np.matmul(rx[i], rx[i-1]) #Reescrivim un valor pel producte de les seves matrius de rotació
        #En aquest loop es garanteix que l'element rx[i] provingui de la multiplicació de les i-1 matrius anteriors

#Matrius de rotació total que s'han d'aplicar a cada mesura.
rot = np.matmul(np.matmul(rx, ry), rz) #Provenen del producte de les tres matrius

#Vectors acceleració a cada instant de temps
a = (np.array([list(ax), list(ay), list(az)])).T

#Transformem els vectors d'acceleració al sistema de referència inicial
a_trans = np.array([np.matmul(rot[i], a[i]) for i in range(len(time))])
#Ja podem integrar!


# Define the function dv/dt = -a
def dvdt(t, v, a):
    return -a

# Define the time range and acceleration values

# Define the initial velocity
v0 = 0

# Solve the differential equation using solve_ivp
sol = spint.solve_ivp(dvdt, [time[0], time[-1]], [v0]*len(time), t_eval=time, args=(a_trans[:,0],), dense_output=True)

# Extract the velocity values at each time point
vx = sol.y[0]

print(vx)

plt.plot(time,vx)
#plt.plot(time, ox)
#plt.plot(time, oy)
#plt.plot(time, oz)
plt.ylabel("vel (m/s)")
plt.xlabel("t (s)")
plt.show()


'''

'''