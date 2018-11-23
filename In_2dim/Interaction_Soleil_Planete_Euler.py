#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------
"""
Author : Mohamed

Title : Interaction entre soleil et une autre planète.

Description : Simuler l'interaction de deux objets avec la méthode d'Euler

"""
#-----------------------------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from objet import *  # Importer la classe objet de fichier objet.py

#----------------------------------------------------------------------------------------------------------

# Definition des objets

#-------------------------

soleil = objet("Soleil", 1.989*1e30, 0, 0, 0, 0) #(nom, masse, x, y, vx, vy)

terre = objet ("Terre", 5.972*1e24, -0.7528373239252,  0.6375222355089,  -0.0113914294224, -0.0131912591762)

print(terre.x0**2 + terre.y0**2)

#----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------

# Integration des equations de newton par méthode d'euler

#-------------------------

dt = 1 #step
T = int(365/dt)*2 # (Nombre de steps)<-> Periode d'integration

#Definition des tableau
terre.x = np.zeros(T); terre.x[0] = terre.x0
terre.y = np.zeros(T); terre.y[0] = terre.y0

terre.vx = np.zeros(T); terre.vx[0] = terre.vx0
terre.vy = np.zeros(T); terre.vy[0] = terre.vy0

#Implementation de la methode d'Euler
for i in range(T-1): 

	terre.vx[i+1] = terre.vx[i] + dt*fx(soleil.masse, terre.x[i], terre.y[i])
	terre.vy[i+1] = terre.vy[i] + dt*fy(soleil.masse, terre.x[i], terre.y[i])

	terre.x[i+1] = terre.x[i] + dt*terre.vx[i]
	terre.y[i+1] = terre.y[i] + dt*terre.vy[i]

#----------------------------------------------------------------------------------------------------


#Plots    
fig1, ax1 = plt.subplots()        
ax1.plot(terre.x, terre.y)

fig2, ax2 = plt.subplots()

t = np.linspace(1,T,T)
ax2.plot(t, E(soleil.masse, terre.x, terre.y, terre.vx, terre.vy))

plt.show()