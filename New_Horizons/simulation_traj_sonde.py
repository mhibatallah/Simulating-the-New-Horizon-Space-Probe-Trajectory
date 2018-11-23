#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------
"""
Author : Mohamed

Title : Simulation de trajectoire de New Horizons

Description : Ici on essayera de simuler la trajde New Horizons en utilisants les données des planètes

"""
#-----------------------------------------------------------------------------------------------------------

from objet import *  # Importer la classe objet de fichier objet.py
import numpy as np
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------------
# Definition de systeme solaire
#-------------------------

bodies = np.array([objet() for i in range(10)])  #Creation d'une liste des objets (on a au total 10 objets: soleil et 8 planetes et Pluto)

data = np.genfromtxt("initial_conditions_solarsystem.txt", usecols=(1,2,3,4,5,6,7), skip_header=1) #On ne peut pas importer du texte avec genfromtxt
names = np.loadtxt("names_solarsystem.txt", dtype = str, skiprows=1, usecols=(1,))

Nbr_obj = len(bodies)

#Definition des parametres de chaque objet
for i in range(Nbr_obj):
	bodies[i].nom = names[i][2:-1] # [2:-1] pour supprimer les caracteres indesires
	bodies[i].masse = data[i][0]
	bodies[i].x0 = data[i][1]
	bodies[i].y0 = data[i][2]
	bodies[i].z0 = data[i][3] 
	bodies[i].vx0 = data[i][4]
	bodies[i].vy0 = data[i][5]
	bodies[i].vz0 = data[i][6]

#[End]----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
# Definition de la sonde
#-------------------------

sonde = objet("New Horizons", 478,-4.848633330340065E-01,  8.564042505568761E-01, -1.037397594205054E-04 ,-2.155445266674756E-02, -1.228323707493898E-02,  3.737740857827989E-04)

#[End]----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
# Importer l'orbite reelle de la sonde
#-------------------------


#[End]----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
# Simuler les trajectoires des planètes a l'aide de Verlet
#-------------------------

dt = 0.1 #step
T = int(410/dt) # (Nombre de steps)<-> Periode d'integration

#Definition des tableaux
for i in range(Nbr_obj):
	bodies[i].x = np.zeros(T); bodies[i].x[0] = bodies[i].x0
	bodies[i].y = np.zeros(T); bodies[i].y[0] = bodies[i].y0
	bodies[i].z = np.zeros(T); bodies[i].z[0] = bodies[i].z0


	bodies[i].vx = np.zeros(T); bodies[i].vx[0] = bodies[i].vx0
	bodies[i].vy = np.zeros(T); bodies[i].vy[0] = bodies[i].vy0
	bodies[i].vz = np.zeros(T); bodies[i].vz[0] = bodies[i].vz0

#Def des v_demi pour chaque objet
vx_demi = np.zeros(Nbr_obj)
vy_demi = np.zeros(Nbr_obj)
vz_demi = np.zeros(Nbr_obj)

#Implementation de l'integrateur de Verlet pour chaque objet (sauf le soleil)
for j in range(T-1): 

	for i in range(1,Nbr_obj): #Modification des parametres pour chaque objet a un instant donne

		#Récupération de l'acceleration
		fx_j, fy_j, fz_j = acceleration_sol(bodies, i, j) #L'acceleration au pas j relative à l'objet i
		
		#Definition des variables de milieux
		vx_demi[i] = bodies[i].vx[j] + (dt/2)*fx_j
		vy_demi[i] = bodies[i].vy[j] + (dt/2)*fy_j
		vz_demi[i] = bodies[i].vz[j] + (dt/2)*fz_j

		# Affectation des positions à l'indice i+1
		bodies[i].x[j+1] = bodies[i].x[j] + dt*vx_demi[i]
		bodies[i].y[j+1] = bodies[i].y[j] + dt*vy_demi[i]
		bodies[i].z[j+1] = bodies[i].z[j] + dt*vz_demi[i]

	for i in range(1,Nbr_obj):

		#L'acceleration au pas i+1 relative à l'objet j
		fx_jplus1, fy_jplus1, fz_jplus1 = acceleration_sol(bodies, i, j+1) #Il faut faire cette étape après le calcul de position à l'indice i+1

		bodies[i].vx[j+1] = vx_demi[i] + (dt/2)*fx_jplus1
		bodies[i].vy[j+1] = vy_demi[i] + (dt/2)*fy_jplus1
		bodies[i].vz[j+1] = vz_demi[i] + (dt/2)*fz_jplus1
#[End]----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
# Interpolation des trajectoires des planetes + Plot
#-------------------------

# from scipy.interpolate import InterpolatedUnivariateSpline

# for i in range(Nbr_obj):

# 	#Redefinition de pas
# 	dt = 1 #step de la sonde aussi
# 	T = int(365/dt)*10 # (Nombre de steps)<-> Periode d'integration
# 	t = np.linspace(1,T,T)*dt

# 	x_interpol = InterpolatedUnivariateSpline(t, bodies[i].x)
# 	y_interpol = InterpolatedUnivariateSpline(t, bodies[i].y)

# 	#Redefinition de pas
# 	dt = 0.1 #step de la sonde aussi
# 	T = int(365/dt)*10 # (Nombre de steps)<-> Periode d'integration
# 	t = np.linspace(1,T,T)*dt

# 	bodies[i].x = x_interpol(t)
# 	bodies[i].y = y_interpol(t)

for i in range(1,Nbr_obj):	
	plt.plot(bodies[i].x, bodies[i].y, label = bodies[i].nom)
	plt.plot(bodies[i].x[-1], bodies[i].y[-1], "b*")

#[End]----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
# Simuler la trajectoire de la sonde
#-------------------------

# #Periode et le pas predefini par l'interpolation juste dans le bloc en haut
# dt = 0.1 #step de la sonde aussi
# T = int(365/dt)*10 # (Nombre de steps)<-> Periode d'integration
# #----------------------------------

#Definition des tableaux
sonde.x = np.zeros(T); sonde.x[0] = sonde.x0
sonde.y = np.zeros(T); sonde.y[0] = sonde.y0
sonde.z = np.zeros(T); sonde.z[0] = sonde.z0

sonde.vx = np.zeros(T); sonde.vx[0] = sonde.vx0
sonde.vy = np.zeros(T); sonde.vy[0] = sonde.vy0
sonde.vz = np.zeros(T); sonde.vz[0] = sonde.vz0


#Def des v_demi Pour la sonde
vx_demi = 0
vy_demi = 0
vz_demi = 0

#Implementation de l'integrateur de Verlet
for j in range(T-1): 

#Definition des variables de milieux
	fx_j, fy_j, fz_j = acceleration_obj(bodies, sonde, j) #L'acceleration au pas j relative à l'objet "obj"

	vx_demi = sonde.vx[j] + (dt/2)*fx_j
	vy_demi = sonde.vy[j] + (dt/2)*fy_j
	vz_demi = sonde.vz[j] + (dt/2)*fz_j

# Affectation des positions à l'indice i+1
	sonde.x[j+1] = sonde.x[j] + dt*vx_demi
	sonde.y[j+1] = sonde.y[j] + dt*vy_demi
	sonde.z[j+1] = sonde.z[j] + dt*vz_demi

	fx_jplus1, fy_jplus1, fz_jplus1 = acceleration_obj(bodies, sonde, j+1) 

#Affectation des vitesses à l'indice i+1
	sonde.vx[j+1] = vx_demi + (dt/2)*fx_jplus1
	sonde.vy[j+1] = vy_demi + (dt/2)*fy_jplus1
	sonde.vz[j+1] = vz_demi + (dt/2)*fz_jplus1

#[End]----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
# Plot de traj de sonde
#------------------------
plt.plot(sonde.x, sonde.y, label="Trajectoire sonde")

plt.gca().set_aspect('equal', adjustable='box') #equal ratios of x and y

plt.legend()
plt.show()

#[End]----------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------------
# Comparaison entre les trajectoires simulees et reelles
#-------------------------



#[End]----------------------------------------------------------------------------------------------------