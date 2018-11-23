#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------
"""
Author : Mohamed

Title : Interaction entre soleil et une autre planète.

Description : Simuler l'interaction de deux objets avec Runge Kutta 2

"""
#-----------------------------------------------------------------------------------------------------------

from objet import *  # Importer la classe objet de fichier objet.py
import numpy as np
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------------

# Definition des objets

#-------------------------

soleil = objet("Soleil", 1.989*1e30, 0, 0, 0, 0) #(nom, masse, x, y, vx, vy)

terre = objet ("Terre", 5.972*1e24, -0.7528373239252,  0.6375222355089,  -0.0113914294224, -0.0131912591762)

print(terre.x0**2 + terre.y0**2)

#----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------

# Integration des equations de newton par Runge Kutta2

#-------------------------

dt = 1 #step
T = int(365/dt) # (Nombre de steps)<-> Periode d'integration

#Definition des tableau
terre.x = np.zeros(T); terre.x[0] = terre.x0
terre.y = np.zeros(T); terre.y[0] = terre.y0

terre.vx = np.zeros(T); terre.vx[0] = terre.vx0
terre.vy = np.zeros(T); terre.vy[0] = terre.vy0

#Implementation de la methode de Runge-Kutta
for i in range(T-1): 

#Definition des variables de milieux

	vx_demi = terre.vx[i] + (dt/2)*fx(soleil.masse, terre.x[i], terre.y[i])
	vy_demi = terre.vy[i] + (dt/2)*fy(soleil.masse, terre.x[i], terre.y[i])

	x_demi = terre.x[i] + (dt/2)*terre.vx[i]
	y_demi = terre.y[i] + (dt/2)*terre.vy[i]

# Affectation des positions à l'indice i+1

	terre.vx[i+1] = terre.vx[i] + dt*fx(soleil.masse, x_demi, y_demi)
	terre.vy[i+1] = terre.vy[i] + dt*fy(soleil.masse, x_demi, y_demi)

	terre.x[i+1] = terre.x[i] + dt*vx_demi
	terre.y[i+1] = terre.y[i] + dt*vy_demi

plt.plot(terre.x, terre.y)
plt.show()

#----------------------------------------------------------------------------------------------------
