#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------
"""
Author : Mohamed

Title : Classe des objets gravitants

Description : elle permet d'associer à chaque objet une classe qui le caractèrise.

"""
#-----------------------------------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

class objet:
	""" Classe représentant les objets qui influence par la gravitation
		Attributs:
		nom 
		masse: Kg
		position (x, y, z): au
		vitesse (v_x, v_y, v_z) : au/day
	"""

	nom = "objet"
	masse = None
	x0 = 0
	y0 = 0
	z0 = 0
	vx0 = 0
	vy0 = 0
	vz0 = 0
	#Listes des positions et vitesse 
	x = None 
	y = None
	z = None
	vx = None
	vy = None 
	vz = None

	#Fonctions interpolees qui contient les coordonnee
	x_interpol = None
	y_interpol = None
	z_interpol = None

	def __init__(self, nom = "objet", masse = None, x0 = 0, y0 = 0, z0 = 0, vx0 = 0, vy0 = 0, vz0 = 0):
		"""Constructeur de notre classe"""
		self.nom = nom
		self.masse = masse
		self.x0 = x0
		self.y0 = y0
		self.z0 = z0
		self.vx0 = vx0
		self.vy0 = vy0
		self.vz0 = vz0


au = 1.49597870e11 #Unité astronomique
jour = 24*3600 #Un jour

G = 6.67408e-11 #Constante gravitationelle 


#Definition de fonction fx(M,x,y,z) et fy(M,x,y,z)
def fx(M,x,y,z=0):
	"""
	Retourne l'acceleration gravitationnelle suivant x dû à un objet de masse M distants de l'objet étudié de x**2+y**2+z**2
	"""
	return -((G*M)/(x**2+y**2+z**2)**(3/2))*x*(jour**2/au**3)

def fy(M,x,y,z=0):
	"""
	Retourne l'acceleration gravitationnelle suivant y dû à un objet de masse M distants de l'objet étudié de x**2+y**2+z**2
	"""
	return -((G*M)/(x**2+y**2+z**2)**(3/2))*y*(jour**2/au**3)

def fz(M,x,y,z=0):
	"""
	Retourne l'acceleration gravitationnelle suivant z dû à un objet de masse M distants de l'objet étudié de x**2+y**2+z**2
	"""
	return -((G*M)/(x**2+y**2+z**2)**(3/2))*z*(jour**2/au**3)

def E(M, x, y, z, vx, vy, vz):
	"""
	Calculer l'energie massique d'un objet sous effet d'un seul objet de masse M
	"""
	return 0.5*(vx**2+vy**2+vz**2)*(au**2/jour**2)-(G*M)/(np.sqrt(x**2+y**2+z**2)*au)
E = np.vectorize(E) #Vectoriser une fonction est benefique en terme de performance et memoire

def pot(M, x, y, z=0):
	"""
	Retourne le potentiel massique d'un objet par rapport à un autre objet de masse M et distant de x**2+y**2+z**2
	"""
	return -(G*M)/(np.sqrt(x**2+y**2+z**2)*au)

pot = np.vectorize(pot)

#----------------------------------------------------------------------------------------------------------
# Multiple objects manipulation
#-------------------------

def acceleration(bodies, i, j):
	"""
	Calculer l'acceleration relative à un objet bodies[i]
	bodies: tous les objets
	i: index of concerned body which undergoes the gravitation of other objects.
	j: index of the step
	"""
	N = len(bodies)

	ax = 0; ay = 0; az = 0 #L'acceleration

	for ip in range(N):
		#Chaque objet bodies[ip] applique une force de gravitation sur l'objet bodies[i] 

		if ip == i: #On veut que pas avoir le même objet bodies[ip]
			continue

		# print(fx(bodies[ip].masse, bodies[i].x[j], bodies[i].y[j]-bodies[ip].y[j], bodies[i].z[j]))
		ax += fx(bodies[ip].masse, bodies[i].x[j]-bodies[ip].x[j], bodies[i].y[j]-bodies[ip].y[j], bodies[i].z[j]-bodies[ip].z[j])
		ay += fy(bodies[ip].masse, bodies[i].x[j]-bodies[ip].x[j], bodies[i].y[j]-bodies[ip].y[j], bodies[i].z[j]-bodies[ip].z[j])
		az += fz(bodies[ip].masse, bodies[i].x[j]-bodies[ip].x[j], bodies[i].y[j]-bodies[ip].y[j], bodies[i].z[j]-bodies[ip].z[j])

	return (ax, ay, az)

def acceleration_obj(bodies, obj, j):
	"""
	Calculer l'acceleration relative à un "obj"
	bodies: tous les objets
	obj: index of concerned body which undergoes the gravitation of other objects.
	j: index of the step
	"""
	N = len(bodies)

	ax = 0; ay = 0; az = 0 #L'acceleration

	for ip in range(N):
		#Chaque objet bodies[ip] applique une force de gravitation sur l'objet object() 

		ax += fx(bodies[ip].masse, obj.x[j]-bodies[ip].x[j], obj.y[j]-bodies[ip].y[j], obj.z[j]-bodies[ip].z[j])
		ay += fy(bodies[ip].masse, obj.x[j]-bodies[ip].x[j], obj.y[j]-bodies[ip].y[j], obj.z[j]-bodies[ip].z[j])
		az += fz(bodies[ip].masse, obj.x[j]-bodies[ip].x[j], obj.y[j]-bodies[ip].y[j], obj.z[j]-bodies[ip].z[j])

	return (ax, ay, az)

def acceleration_sol(bodies, i, j):
	"""
	Calculer l'acceleration relative à un objet bodies[i] avec effet de soleil seulement
	bodies: tous les objets
	i: index of concerned body which undergoes the gravitation of other objects.
	j: index of the step
	"""
	ax = fx(bodies[0].masse, bodies[i].x[j], bodies[i].y[j], bodies[i].z[j])
	ay = fy(bodies[0].masse, bodies[i].x[j], bodies[i].y[j], bodies[i].z[j])
	az = fz(bodies[0].masse, bodies[i].x[j], bodies[i].y[j], bodies[i].z[j])

	return (ax, ay, az)

def acceleration_interpol(bodies, t, x, y, z):
	"""
	Calculer l'acceleration relative a la sonde de coord x,y,z a l'instant t
	Les coord des objets sont stockes dans la methode x/y/z_interpol qui prend comme parametre un instant donne
	"""

	N = len(bodies)

	ax = 0; ay = 0; az = 0 #L'acceleration

	for ip in range(N):
		#Chaque objet bodies[ip] applique une force de gravitation sur l'objet object() 

		ax += fx(bodies[ip].masse, x-bodies[ip].x_interpol(t), y-bodies[ip].y_interpol(t), z-bodies[ip].z_interpol(t))
		ay += fy(bodies[ip].masse, x-bodies[ip].x_interpol(t), y-bodies[ip].y_interpol(t), z-bodies[ip].z_interpol(t))
		az += fz(bodies[ip].masse, x-bodies[ip].x_interpol(t), y-bodies[ip].y_interpol(t), z-bodies[ip].z_interpol(t))

	return (ax, ay, az)

def Energy_sol(bodies,i):
	"""
	L'Energie massique d'un objet sous l'effet de soleil seulement.
	"""
	potential = pot(bodies[0].masse, bodies[i].x, bodies[i].y, bodies[i].z)

	return 0.5*(au**2/jour**2)*(bodies[i].vx**2+bodies[i].vy**2+bodies[i].vz**2)+potential

def Energy(bodies, i):

	"""
	L'Energie massique d'un objet sous l'effet d'autres objet qui lui entoure.
	"""

	N = len(bodies)

	potential = 0

	# potential = pot(bodies[0].masse, bodies[i].x, bodies[i].y, bodies[i].z)

	for ip in range(N):
		if ip == i:
			continue
		potential += pot(bodies[ip].masse, bodies[i].x-bodies[ip].x, bodies[i].y-bodies[ip].y, bodies[i].z-bodies[ip].z)
	
	return 0.5*(au**2/jour**2)*(bodies[i].vx**2+bodies[i].vy**2+bodies[i].vz**2)+potential	

#[End]----------------------------------------------------------------------------------------------------	


#----------------------------------------------------------------------------------------------------------
# The adaptive verlet method
#-------------------------

def rho(M, x, y, z, vx, vy, vz):

	# return np.sqrt((au**2/jour**2)*(vx**2+vy**2+vz**2)+((G*M)/((x**2+y**2+z**2)*(au**2)))**2)
	f=(G*M)/((x**2+y**2+z**2)*(au**2))
	# return (f+0.0001)/((f+0.0001)+1)
	return f
	# return (x**2+y**2+z**2)*(au**2)/(1+((x**2+y**2+z**2)*(au**2)))
def rho_obj(bodies, obj, j, t):
	"""
	Calculer le configurateur de pas rho
	bodies: tous les objets
	obj: the concerned body which undergoes the gravitation of other objects.
	j: index of the step
	t: temps
	"""
	N = len(bodies)

	rho1 = 0 #pas le meme nom que la fonction rho

	for ip in range(N):
		#Chaque objet bodies[ip]
		rho1 = rho1 + rho(bodies[ip].masse, obj.x[j]-bodies[ip].x_interpol(t), obj.y[j]-bodies[ip].y_interpol(t), obj.z[j]-bodies[ip].z_interpol(t), obj.vx[j], obj.vy[j], obj.vz[j])

	# return rho1
	# return (rho1+0.0001)/((rho1+0.0001)+1)
	return np.sqrt(rho1**2+0.0001**2)/(np.sqrt(rho1**2+0.0001**2)+1)
#[End]----------------------------------------------------------------------------------------------------

	