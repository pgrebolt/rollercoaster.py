# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 15:24:00 2023

@author: Pau Grèbol Tomàs
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import ode
from scipy.spatial.transform import Rotation as R
import scipy.interpolate

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

def odes(t, solution, data, time_mes):

    '''
    Aquesta és la funció que torna les derivades a cada punt. En total tenim un sistema de 3 odes: do/dt, dx/dt i dv/dt
    '''

    #Extraiem els valors de solution. Aquests són els valors de les derivades: angle, velocitat, posició
    theta = solution[:3] #angles de rotació a cada eix (EN PRINCIPI NO ESTAN LIMITATS EN (-2PI, +2PI)
    v = solution[3:6] #velocitat lineal (amb el canvi de sistema de referència fet)
    x = solution[6:9] #posició (amb el canvi de sistema de referència fet)

    #Extraiem els valors mesurats
    w_mes = data[:3]
    a_mes = data[3:6]

    #Extrapolem els valors de w i a al punt on s'està integrant
    w = scipy.interpolate.interp1d(time_mes, w_mes, kind='linear')(t)
    a = scipy.interpolate.interp1d(time_mes, a_mes, kind='linear')(t)

    '''
    Rotem el vector acceleració per passar-lo al sistema de referència inicial
    '''
    # Matrius de rotació en cada eix
    rx, ry, rz = R.from_euler('x', theta[0]).as_matrix(), R.from_euler('y', theta[1]).as_matrix(), \
        R.from_euler('z', theta[2]).as_matrix()
    # Aquests elements contenen les matrius de rotació que cal aplicar a cada punt, però les velocitats estan mesurades a partir de la posició
    # anterior. Per trobar-ho respecte la posició inicial cal aplicar successives rotacions

    # Matrius de rotació total que s'han d'aplicar a cada mesura.
    rot = np.matmul(np.matmul(rx, ry), rz)  # Provenen del producte de les tres matrius
    rot = rx.dot(ry.dot(rz))

    #Rotem el vector acceleració
    a_rot = rot.dot(a)

    #Matriu on hi guardem els valors de les derivades
    derivatives = np.zeros(6)
    derivatives[:3] = w #derivada de l'angle és la velocitat angular
    derivatives[3:6] = a_rot #derivada de la velocitat és l'acceleració (lineals)
    #derivatives[6:9] = v #derivada de la posició és la velocitat lineal

    return derivatives

results, t_results = [], [] #Arrays on hi guardarem els resultats de la integració
def solout(t, solution):
    '''
    Aquesta funció s'executa cada vegada que es completa un pas d'integració.
    Nosaltres la fem servir per guardar els valors de la solució a cada instant de temps.
    '''
    #Guardem els resultats d'aquest pas d'integració
    results.extend([solution.copy()])
    t_results.extend([t])

    #Seguim integrant (si fem return -1 s'atura la integració)
    return 0


'''
    Resolem el sistema d'equacions diferencials
'''

#Definim el mètode d'integració numèrica i els seus paràmetres
X = np.zeros((6, 1)) #tots els valors inicials d'angle, velocitat i posició són 0
t0 = np.min(time) #temps inicial és 0

data = np.array([wx, wy, wz, ax, ay, az]) #Valors mesurats

solver = ode(odes).set_integrator('dopri5', first_step = tvar[1], max_step = np.max(tvar), rtol = 1e-5)
solver.set_initial_value(X, t0).set_f_params(data, time)
solver.set_solout(solout)

#Aquí es fa la integració
solver.integrate(np.max(time))

'''
Fem el plot dels resultats
'''

#Extraiem els valors de la integració
theta = results[:3]
v = results[3:6]
x = results[6:9]

plt.plot(time,v[0])
#plt.plot(time, ox)
#plt.plot(time, oy)
#plt.plot(time, oz)
plt.ylabel("vel (m/s)")
plt.xlabel("t (s)")
plt.show()
