#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------
"""
Author : Mohamed

Title : Comparaison entre orbit d'une planete simulee et orbite reelle

"""
#-----------------------------------------------------------------------------------------------------------

from objet import *  # Importer la classe objet de fichier objet.py
import numpy as np
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------------

# Definition des objets

#-------------------------

soleil = objet("Soleil", 1.989*1e30, 0, 0, 0, 0, 0 ,0) #(nom, masse, x, y, z, vx, vy, vz)

# planet = objet ("Mercury", 3.285E+23, 0.3083240304,	-0.2675876914,	-0.0501631296,	0.0128726775,	0.0225451404,	0.0006491183)
planet = objet ("Earth", 5.972*1e24,-0.9284315306,0.3454175562,2.83E-06,-0.0062791364,-0.0161974643,6.12E-07)
# planet = objet ("Venus", 5.972*1e24,-0.5782373235144,    0.4247691032278,    0.0391370335663,   -0.0120522628525,   -0.0164029924898,    0.0004745264781)
# print(planet.x0**2 + planet.y0**2 + planet.z0**2)

#----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------

# Intergration using the adaptive verlet

#-------------------------

ds = 1000 #step
T = int(365) # (Nombre de steps)<-> Periode d'integration

#Definition des tableaux
planet.x = np.zeros(1); planet.x[0] = planet.x0
planet.y = np.zeros(1); planet.y[0] = planet.y0
planet.z = np.zeros(1); planet.z[0] = planet.z0

planet.vx = np.zeros(1); planet.vx[0] = planet.vx0
planet.vy = np.zeros(1); planet.vy[0] = planet.vy0
planet.vz = np.zeros(1); planet.vz[0] = planet.vz0

#Time array
time = np.zeros(1)


#Def des v_demi et x_demi pour l'objet
vx_demi = 0
vy_demi = 0
vz_demi = 0

x_demi = 0
y_demi = 0
z_demi = 0

#Implementation de l'integrateur de Verlet

i = 0
rho1 = rho(soleil.masse, planet.x0, planet.y0, planet.z0, planet.vx0, planet.vy0, planet.vz0)

while time[i] < T:

#Define Rho 1 -> rho[i]
	if i>0:
		rho1 = rho2

#Definition des variables de milieux

	x_demi = planet.x[i] + (ds/(2*rho1))*planet.vx[i]
	y_demi = planet.y[i] + (ds/(2*rho1))*planet.vy[i]
	z_demi = planet.z[i] + (ds/(2*rho1))*planet.vz[i]

	vx_demi = planet.vx[i] + (ds/(2*rho1))*fx(soleil.masse, x_demi, y_demi, z_demi)
	vy_demi = planet.vy[i] + (ds/(2*rho1))*fy(soleil.masse, x_demi, y_demi, z_demi)
	vz_demi = planet.vz[i] + (ds/(2*rho1))*fz(soleil.masse, x_demi, y_demi, z_demi)

#Define Rho 2 -> rho[i+1]
	
	rho2 = 2*rho(soleil.masse, x_demi, y_demi, z_demi, vx_demi, vy_demi, vz_demi) - rho1


# Affectation des positions à l'indice i+1
	planet.vx = np.append(planet.vx , vx_demi + (ds/(2*rho2))*fx(soleil.masse, x_demi, y_demi, z_demi))
	planet.vy =np.append(planet.vy , vy_demi + (ds/(2*rho2))*fy(soleil.masse, x_demi, y_demi, z_demi))
	planet.vz = np.append(planet.vz , vz_demi + (ds/(2*rho2))*fz(soleil.masse, x_demi, y_demi, z_demi))

	planet.x = np.append(planet.x , x_demi + (ds/(2*rho2))*planet.vx[i+1])
	planet.y = np.append(planet.y , y_demi + (ds/(2*rho2))*planet.vy[i+1])
	planet.z = np.append(planet.z , z_demi + (ds/(2*rho2))*planet.vz[i+1])

# Affectation de temps
	
	time = np.append(time, time[i]+((ds/2)*(1/rho1 + 1/rho2)))

#incrementation
	i = i+1

# plt.plot(planet.x, planet.y, label="simulated")

plt.plot(np.diff(time))

plt.show()

#----------------------------------------------------------------------------------------------------

