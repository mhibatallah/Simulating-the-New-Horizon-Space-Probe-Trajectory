#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------
"""
Author : Mohamed

Title : Simulation de trajectoire de New Horizons

Description : Ici on essayera de simuler la trajetoire New Horizons

"""
#-----------------------------------------------------------------------------------------------------------

from objet import *  # Importer la classe objet de fichier objet.py
import numpy as np
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------------
# Definition de systeme solaire
#-------------------------

bodies = np.array([objet() for i in range(10)])  #Creation d'une liste des objets (on a au total 10 objets:soleil et 8 planetes et Pluto)

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

# sonde = objet("New Horizons", 478,-4.848633330340065E-01,  8.564042505568761E-01, -1.037397594205054E-04 ,-2.155445266674756E-02, -1.228323707493898E-02,  3.737740857827989E-04)

#Coordinates in heliocentric
# sonde = objet("New Horizons", 478,-4.886893778728491E-01,  8.540814037081539E-01,  1.377446004041602E-05, -2.155158733368952E-02, -1.228948289664512E-02,  3.737717394886807E-04) #Geometric

# sonde = objet("New Horizons", 478,-4.885668712456782E-01,  8.541512107925574E-01,  1.165010059172766E-05, -2.155488459027918E-02, -1.228932883519473E-02,  3.738220209383381E-04) #Astrometric

sonde = objet("New Horizons", 478,-4.885668682172510E-01,  8.541512125247905E-01,  1.165011346557786E-05, -2.155488459027918E-02, -1.228932883519473E-02,  3.738220209383381E-04) #Apparent

#[End]----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
# Simuler les trajectoires des planètes a l'aide de Verlet
#-------------------------

dt = 1 #step
T = int((365*9+200)/dt) # (Nombre de steps)<-> Periode d'integration

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
# Interpolation des trajectoires des sondees + Plot
#-------------------------

from scipy.interpolate import UnivariateSpline

for i in range(Nbr_obj):

	t = np.linspace(1,T,T)*dt #Def des intervalles

	bodies[i].x_interpol = UnivariateSpline(t, bodies[i].x, s=0)
	bodies[i].y_interpol = UnivariateSpline(t, bodies[i].y, s=0)
	bodies[i].z_interpol = UnivariateSpline(t, bodies[i].z, s=0)

#Plot des traj interpolee
for i in range(1,Nbr_obj):	
	plt.plot(bodies[i].x_interpol(t), bodies[i].y_interpol(t), label = bodies[i].nom) 
	plt.plot(bodies[i].x[-1], bodies[i].y[-1], "b*")

plt.plot(bodies[5].x[int(409/dt)], bodies[5].y[int(409/dt)], "k*") #Jupiter

#[End]----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
# Import de traj réelle
#-------------------------

#Traj Horizon reelle
x, y, z, vx, vy, vz = np.genfromtxt("horizons_results.txt", usecols=(2,3,4,5,6,7), unpack=True, delimiter=",") 
plt.plot(x, y, label = "Trajectoire sonde réelle")

#Interpolation
N = len(x)

t = np.linspace(1,N,N) #Def des intervalles dt = 1
x_ = UnivariateSpline(t, x, s=0)
y_ = UnivariateSpline(t, y, s=0)
z_ = UnivariateSpline(t, z, s=0)
vx_ = UnivariateSpline(t, vx, s=0)
vy_ = UnivariateSpline(t, vy, s=0)
vz_ = UnivariateSpline(t, vz, s=0)


#[End]----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
# Simuler la trajectoire de la sonde par adaptive verlet
#-------------------------

ds = 0.0001 #step parametrique
T = 365*9+200 #(Nombre de steps)<->Periode d'integration

#Definition des tableaux 
sonde.x = np.zeros(1); sonde.x[0] = sonde.x0
sonde.y = np.zeros(1); sonde.y[0] = sonde.y0
sonde.z = np.zeros(1); sonde.z[0] = sonde.z0

sonde.vx = np.zeros(1); sonde.vx[0] = sonde.vx0 
sonde.vy = np.zeros(1); sonde.vy[0] = sonde.vy0 
sonde.vz = np.zeros(1); sonde.vz[0] = sonde.vz0

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

i = 0 #count for time
j = 0 #count for number of corrections

# rho1 = rho(bodies[0].masse, sonde.x0, sonde.y0, sonde.z0, sonde.vx0, sonde.vy0, sonde.vz0)

rho1 = rho_obj(bodies, sonde, 0, time[0])

while time[i] < T:

#Define Rho 1 -> rho[i]
	if i>0:
		rho1 = rho2

#Definition des variables de milieux

	x_demi = sonde.x[i] + (ds/(2*rho1))*sonde.vx[i]
	y_demi = sonde.y[i] + (ds/(2*rho1))*sonde.vy[i]
	z_demi = sonde.z[i] + (ds/(2*rho1))*sonde.vz[i]

	fx, fy, fz = acceleration_interpol(bodies, time[i], x_demi, y_demi, z_demi)

	vx_demi = sonde.vx[i] + (ds/(2*rho1))*fx
	vy_demi = sonde.vy[i] + (ds/(2*rho1))*fy
	vz_demi = sonde.vz[i] + (ds/(2*rho1))*fz

#Define Rho 2 -> rho[i+1]
	
	# rho2 = 2*rho(bodies[0].masse, x_demi, y_demi, z_demi, vx_demi, vy_demi, vz_demi) - rho1

	rho2 = 2*rho_obj(bodies, sonde, i, time[i]) - rho1

	deltaV_x = 0; deltaV_y = 0; deltaV_z = 0 #initialisation des propulsions

	thruster_deltaV = 2.88774164E-8 #Valeur max de deltaV fournie par un propulseur -> 5 cm/s

	if np.sqrt((sonde.x[i]-x_(time[i]))**2+(sonde.y[i]-y_(time[i]))**2+(sonde.z[i]-z_(time[i]))**2)>0.1 #Verification de la condition:
		deltaV_x = np.min(vx_(time[i])-sonde.vx[i], thruster_deltaV) 
		deltaV_y = np.min(vy_(time[i])-sonde.vy[i], thruster_deltaV) 
		deltaV_z = np.min(vz_(time[i])-sonde.vz[i], thruster_deltaV)

		print(deltaV_x, deltaV_y, deltaV_z)
		j+=1

	# Affectation des positions à l'indice i+1
	sonde.vx = np.append(sonde.vx , vx_demi + (ds/(2*rho2))*fx + deltaV_x)
	sonde.vy = np.append(sonde.vy , vy_demi + (ds/(2*rho2))*fy + deltaV_y)
	sonde.vz = np.append(sonde.vz , vz_demi + (ds/(2*rho2))*fz + deltaV_z)

	sonde.x = np.append(sonde.x , x_demi + (ds/(2*rho2))*sonde.vx[i+1])
	sonde.y = np.append(sonde.y , y_demi + (ds/(2*rho2))*sonde.vy[i+1])
	sonde.z = np.append(sonde.z , z_demi + (ds/(2*rho2))*sonde.vz[i+1])

	# Affectation de temps
	
	time = np.append(time, time[i]+((ds/2)*(1/rho1 + 1/rho2)))


#incrementation
	i = i+1

print(j) #show nbr of corrections	

#[End]----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
# Plot de traj de sonde
#------------------------
plt.plot(sonde.x, sonde.y, label="Trajectoire sonde")

#[End]----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
# Comparaison entre les trajectoires simulees et reelles
#-------------------------

# #Traj Jupyter reelle
# x, y, z = np.genfromtxt("jupyter_results.txt", usecols=(2,3,4), unpack=True, skip_header=1, max_rows=410)
# plt.plot(x, y, label = "Trajectoire Jupyter Réelle")
# plt.plot(x[-1], y[-1], "k*")

plt.xlabel("x (Au)")
plt.ylabel("y (Au)")

plt.gca().set_aspect('equal', adjustable='box') #equal ratios of x and y
plt.legend()


#Comparison real and simulated trajectory Jupyter
# t = np.linspace(1, 410, 410)
# fig,ax = plt.subplots()
# ax.plot(((bodies[5].x_interpol(t)-x)**2+(bodies[5].y_interpol(t)-y)**2))
# plt.show()

# #Plot diff time
# plt.plot(time[:-1], np.diff(time));plt.show()
plt.show()

#[End]----------------------------------------------------------------------------------------------------