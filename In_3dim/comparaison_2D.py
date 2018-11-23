#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------
"""
Author : Mohamed

Title : Comparaison entre orbit d'une planete simulee et orbite reelle

"""
#-----------------------------------------------------------------------------------------------------------

from objet_2D import *  # Importer la classe objet de fichier objet.py
import numpy as np
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------------

# Definition des objets

#-------------------------

soleil = objet("Soleil", 1.989*1e30, 0, 0, 0, 0) #(nom, masse, x, y, z, vx, vy, vz)

# planet = objet ("Mercury", 3.285E+23, 0.3083240304,	-0.2675876914,	-0.0501631296,	0.0128726775,	0.0225451404,	0.0006491183)
# planet = objet ("Earth", 5.972*1e24,-0.9284315306,0.3454175562,2.83E-06,-0.0062791364,-0.0161974643,6.12E-07)
planet = objet ("Venus", 5.972*1e24,-0.5782373235144,    0.4247691032278,    -0.0120522628525,   -0.0164029924898)
# print(planet.x0**2 + planet.y0**2 + planet.z0**2)

#----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------

# Integration des equations de newton par l'integrateur de Verlet

#-------------------------

dt = 1 #step
T = int(365/dt) # (Nombre de steps)<-> Periode d'integration

#Definition des tableaux
planet.x = np.zeros(T); planet.x[0] = planet.x0
planet.y = np.zeros(T); planet.y[0] = planet.y0
# planet.z = np.zeros(T); planet.y[0] = planet.z0

planet.vx = np.zeros(T); planet.vx[0] = planet.vx0
planet.vy = np.zeros(T); planet.vy[0] = planet.vy0
# planet.vz = np.zeros(T); planet.vz[0] = planet.vz0


#Def des v_demi pour chaque objet
vx_demi = 0
vy_demi = 0
# vz_demi = 0

#Implementation de l'integrateur de Verlet
for i in range(T-1): 

#Definition des variables de milieux

	vx_demi = planet.vx[i] + (dt/2)*fx(soleil.masse, planet.x[i], planet.y[i])
	vy_demi = planet.vy[i] + (dt/2)*fy(soleil.masse, planet.x[i], planet.y[i])
	# vz_demi = planet.vz[i] + (dt/2)*fz(soleil.masse, planet.x[i], planet.y[i])

# Affectation des positions à l'indice i+1
	planet.x[i+1] = planet.x[i] + dt*vx_demi
	planet.y[i+1] = planet.y[i] + dt*vy_demi
	# planet.z[i+1] = planet.z[i] + dt*vz_demi

	planet.vx[i+1] = vx_demi + (dt/2)*fx(soleil.masse, planet.x[i+1], planet.y[i+1])
	planet.vy[i+1] = vy_demi + (dt/2)*fy(soleil.masse, planet.x[i+1], planet.y[i+1])
	# planet.vz[i+1] = vz_demi + (dt/2)*fz(soleil.masse, planet.x[i+1], planet.y[i+1], planet.z[i+1])

plt.plot(planet.x, planet.y, label="simulated")

#----------------------------------------------------------------------------------------------------
#Imports des donnes de planetes
# x, y, z, vx, vy, vz = np.genfromtxt("real_simulation_mercury.txt", usecols=(2,3,4,5,6,7), skip_header=1, unpack=True) 
# x, y, z, vx, vy, vz = np.genfromtxt("real_simulation_earth.txt", usecols=(2,3,4,5,6,7), skip_header=1, unpack=True) 
x, y, z, vx, vy, vz = np.genfromtxt("real_simulation_venus.txt", usecols=(2,3,4,5,6,7), skip_header=1, unpack=True) 


plt.plot(x,y, label = "real")


plt.legend()

fig, ax = plt.subplots()
ax.plot(planet.x**2+planet.y**2)


fig, ax = plt.subplots()

Nrg = E(soleil.masse, planet.x, planet.y, planet.vx, planet.vy)
Nrg /= np.abs(Nrg[0])  #Pour Normaliser

t = np.linspace(1,T,T)*dt
ax.plot(t, Nrg)

ax.set_xlabel("t (jour)")
ax.set_ylabel("E/$|E_0|$")

ax.get_yaxis().get_major_formatter().set_useOffset(False) #Disable scaling of values in plot wrt y-axis

print("Energie moyenne = " + str(np.mean(Nrg)) + ", Ecart_Type = " + str(np.std(Nrg)))

plt.show()


