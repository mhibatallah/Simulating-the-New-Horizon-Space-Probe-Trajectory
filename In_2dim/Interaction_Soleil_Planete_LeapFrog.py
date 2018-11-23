#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------
"""
Author : Mohamed

Title : Interaction entre soleil et une autre planète.

Description : Simuler l'interaction de deux objets avec Leap Frog

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

# Integration des equations de newton par LeapFrog

#-------------------------

dt = 2 #step
T = int(365/dt)*10 # (Nombre de steps)<-> Periode d'integration

#Definition des tableau
terre.x = np.zeros(T); terre.x[0] = terre.x0
terre.y = np.zeros(T); terre.y[0] = terre.y0

vx_demi = np.zeros(T); vx_demi[0] = terre.vx0 + (dt/2)*fx(soleil.masse, terre.x0, terre.y0)
vy_demi = np.zeros(T); vy_demi[0] = terre.vx0 + (dt/2)*fy(soleil.masse, terre.x0, terre.y0)

#Implementation de la methode de LeapFrog
for i in range(T-1): 

# Affectation des positions à l'indice i+1
	terre.x[i+1] = terre.x[i] + dt*vx_demi[i]
	terre.y[i+1] = terre.y[i] + dt*vy_demi[i]
    
#Affectation des vitesses:
	vx_demi[i+1] = vx_demi[i] + dt*fx(soleil.masse, terre.x[i+1], terre.y[i+1])
	vy_demi[i+1] = vy_demi[i] + dt*fy(soleil.masse, terre.x[i+1], terre.y[i+1])
    #Affecter les vitesses par celles de milieu
    
	terre.vx = vx_demi; terre.vy = vy_demi

plt.plot(terre.x, terre.y)
plt.show()

#----------------------------------------------------------------------------------------------------


