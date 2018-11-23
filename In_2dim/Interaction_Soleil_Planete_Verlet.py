#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------
"""
Author : Mohamed

Title : Interaction entre soleil et une autre planète.

Description : Simuler l'interaction de deux objets avec Verlet

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
# terre = objet(nom="Terre", masse=3.30E+23, x0=0.3083240304, y0=-0.2675876914, vx0=0.0128726775, vy0=0.0225451404)

print(terre.x0**2 + terre.y0**2)

#----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------

# Integration des equations de newton par l'integrateur de Verlet

#-------------------------

dt = 1 #step
T = int(365/dt) # (Nombre de steps)<-> Periode d'integration

#Definition des tableaux
terre.x = np.zeros(T); terre.x[0] = terre.x0
terre.y = np.zeros(T); terre.y[0] = terre.y0

terre.vx = np.zeros(T); terre.vx[0] = terre.vx0
terre.vy = np.zeros(T); terre.vy[0] = terre.vy0

#Implementation de l'integrateur de Verlet
for i in range(T-1): 

#Definition des variables de milieux

	vx_demi = terre.vx[i] + (dt/2)*fx(soleil.masse, terre.x[i], terre.y[i])
	vy_demi = terre.vy[i] + (dt/2)*fy(soleil.masse, terre.x[i], terre.y[i])

# Affectation des positions à l'indice i+1
	terre.x[i+1] = terre.x[i] + dt*vx_demi
	terre.y[i+1] = terre.y[i] + dt*vy_demi

	terre.vx[i+1] = vx_demi + (dt/2)*fx(soleil.masse, terre.x[i+1], terre.y[i+1])
	terre.vy[i+1] = vy_demi + (dt/2)*fy(soleil.masse, terre.x[i+1], terre.y[i+1])

plt.plot(terre.x, terre.y)

#----------------------------------------------------------------------------------------------------

fig, ax = plt.subplots()

Nrg = E(soleil.masse, terre.x, terre.y, terre.vx, terre.vy)
Nrg /= np.abs(Nrg[0])  #Pour Normaliser

t = np.linspace(1,T,T)*dt
ax.plot(t, Nrg)

ax.set_xlabel("t (jour)")
ax.set_ylabel("E/$|E_0|$")

ax.get_yaxis().get_major_formatter().set_useOffset(False) #Disable scaling of values in plot wrt y-axis

print("Energie moyenne = " + str(np.mean(Nrg)) + ", Ecart_Type = " + str(np.std(Nrg)))

plt.show()
