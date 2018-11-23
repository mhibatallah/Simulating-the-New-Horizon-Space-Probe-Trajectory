#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------
"""
Author : Mohamed

Title : Implementation de systeme solaire

Description : Ici on va essayer de simuler les trajectoires de chaque système solaire

"""
#-----------------------------------------------------------------------------------------------------------


from objet import *  # Importer la classe objet de fichier objet.py
import numpy as np
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------------
# Definition de systeme solaire
#-------------------------

bodies = np.array([objet() for i in range(10)])  #Creation d'une liste des objets (on a au total 9 objets: soleil et 8 planetes)

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
# Simuler les trajectoires à l'aide de Verlet avec effet des planètes
#-------------------------

dt = 0.1 #step
T = int(365/dt)*5 # (Nombre de steps)<-> Periode d'integration

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
		fx_j, fy_j, fz_j = acceleration(bodies, i, j) #L'acceleration au pas j relative à l'objet i
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
		fx_jplus1, fy_jplus1, fz_jplus1 = acceleration(bodies, i, j+1) #Il faut faire cette étape après le calcul de postion à l'indice i+1

		bodies[i].vx[j+1] = vx_demi[i] + (dt/2)*fx_jplus1
		bodies[i].vy[j+1] = vy_demi[i] + (dt/2)*fy_jplus1
		bodies[i].vz[j+1] = vz_demi[i] + (dt/2)*fz_jplus1

#[End]----------------------------------------------------------------------------------------------------

fig1, ax1 = plt.subplots()

# for i in range(1,Nbr_obj):
# 	ax1.plot(bodies[i].x, bodies[i].y, label="Avec couplage")
ax1.plot(bodies[1].x, bodies[1].y, label="Avec couplage")

# plt.gca().set_aspect('equal', adjustable='box') #equal ratios of x and y


#----------------------------------------------------------------------------------------------------------
# Plot NRG cas: avec couplage
#-------------------------
fig, ax = plt.subplots()

Nrg = Energy(bodies, 1) #Changez le numero pour voir l'energie de chaque planete.
Nrg /= np.abs(Nrg[0])  #Pour Normaliser
print(Nrg)

t = np.linspace(1,T,T)*dt
ax.plot(t, Nrg, label = "Avec couplage")

ax.set_xlabel("t (jour)")
ax.set_ylabel("E/$|E_0|$")

ax.get_yaxis().get_major_formatter().set_useOffset(False) #Disable scaling of values in plot wrt y-axis

print("Energie moyenne = " + str(np.mean(Nrg)) + ", Ecart_Type = " + str(np.std(Nrg)))

#[End]----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
# Simuler les trajectoires à l'aide de Verlet sans couplage
#-------------------------

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

#Implementation de l'integrateur de Verlet pour chaque objet
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
		fx_jplus1, fy_jplus1, fz_jplus1 = acceleration_sol(bodies, i, j+1) #Il faut faire cette étape après le calcul de postion à l'indice i+1

		bodies[i].vx[j+1] = vx_demi[i] + (dt/2)*fx_jplus1
		bodies[i].vy[j+1] = vy_demi[i] + (dt/2)*fy_jplus1
		bodies[i].vz[j+1] = vz_demi[i] + (dt/2)*fz_jplus1

#[End]----------------------------------------------------------------------------------------------------

# for i in range(1,Nbr_obj):
# 	ax1.plot(bodies[i].x, bodies[i].y, label="Sans couplage")
ax1.plot(bodies[1].x, bodies[1].y, label="Sans couplage")

# plt.gca().set_aspect('equal', adjustable='box') #equal ratios of x and y
ax1.legend()


#----------------------------------------------------------------------------------------------------------
# Plot NRG cas: sans couplage
#-------------------------
Nrg = Energy(bodies, 1) #Changez le numero pour voir l'energie de chaque planete.
Nrg /= np.abs(Nrg[0])  #Pour Normaliser


t = np.linspace(1,T,T)*dt
ax.plot(t, Nrg,label = "Sans couplage")

ax.set_xlabel("t (jour)")
ax.set_ylabel("E/$|E_0|$")

ax.get_yaxis().get_major_formatter().set_useOffset(False) #Disable scaling of values in plot wrt y-axis

print("Energie moyenne = " + str(np.mean(Nrg)) + ", Ecart_Type = " + str(np.std(Nrg)))

plt.legend()
plt.show()

#[End]----------------------------------------------------------------------------------------------------