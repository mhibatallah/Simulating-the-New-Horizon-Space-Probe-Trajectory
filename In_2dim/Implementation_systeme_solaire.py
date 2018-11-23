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

data = np.genfromtxt("initial_conditions_solarsystem.txt", usecols=(1,2,3,4,5), skip_header=1) #On ne peut pas importer du texte avec genfromtxt
names = np.loadtxt("names_solarsystem.txt", dtype = str, skiprows=1, usecols=(1,))

Nbr_obj = len(bodies) #Nombre d'objets

#Definition des parametres de chaque objet
for i in range(Nbr_obj):
	bodies[i].nom = names[i][2:-1] # [2:-1] pour supprimer les caracteres indesires
	bodies[i].masse = data[i][0]
	bodies[i].x0 = data[i][1]
	bodies[i].y0 = data[i][2]
	bodies[i].vx0 = data[i][3]
	bodies[i].vy0 = data[i][4]


#[End]----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
# Simuler les trajectoires à l'aide de Verlet
#-------------------------

dt = 0.1 #step
T = int(365/dt)*10 # (Nombre de steps)<-> Periode d'integration


#Definition des tableaux
for i in range(Nbr_obj):
	bodies[i].x = np.zeros(T); bodies[i].x[0] = bodies[i].x0
	bodies[i].y = np.zeros(T); bodies[i].y[0] = bodies[i].y0

	bodies[i].vx = np.zeros(T); bodies[i].vx[0] = bodies[i].vx0
	bodies[i].vy = np.zeros(T); bodies[i].vy[0] = bodies[i].vy0

#def des v_demi
vx_demi = np.zeros(Nbr_obj)
vy_demi = np.zeros(Nbr_obj)

#Implementation de l'integrateur de Verlet pour chaque objet (sauf le soleil)
for j in range(T-1): 

	for i in range(1,Nbr_obj): #Modification des parametres pour chaque objet a un instant donne

		fx_j, fy_j = acceleration(bodies, i, j) #L'acceleration au pas j relative à l'objet i

		#Definition des variables de milieux
		vx_demi[i] = bodies[i].vx[j] + (dt/2)*fx_j
		vy_demi[i] = bodies[i].vy[j] + (dt/2)*fy_j

		# Affectation des positions à l'indice i+1
		bodies[i].x[j+1] = bodies[i].x[j] + dt*vx_demi[i]
		bodies[i].y[j+1] = bodies[i].y[j] + dt*vy_demi[i]

	for i in range(1,Nbr_obj):

		#L'acceleration au pas i+1 relative à l'objet j
		fx_jplus1, fy_jplus1 = acceleration(bodies, i, j+1) #Il faut faire cette étape après le calcul de postion à l'indice i+1

		bodies[i].vx[j+1] = vx_demi[i] + (dt/2)*fx_jplus1
		bodies[i].vy[j+1] = vy_demi[i] + (dt/2)*fy_jplus1



#[End]----------------------------------------------------------------------------------------------------

for i in range(1,Nbr_obj):
	plt.plot(bodies[i].x, bodies[i].y)

plt.gca().set_aspect('equal', adjustable='box') #equal ratios of x and y


#Plot NRG
fig, ax = plt.subplots()

Nrg = Energy(bodies, 1) #Changez le numero pour voir l'energie de chaque planete.
Nrg /= np.abs(Nrg[0])  #Pour Normaliser

t = np.linspace(1,T,T)*dt
ax.plot(t, Nrg)

ax.set_xlabel("t (jour)")
ax.set_ylabel("E/$|E_0|$")

ax.get_yaxis().get_major_formatter().set_useOffset(False) #Disable scaling of values in plot wrt y-axis

print("Energie moyenne = " + str(np.mean(Nrg)) + ", Ecart_Type = " + str(np.std(Nrg)))

plt.show()