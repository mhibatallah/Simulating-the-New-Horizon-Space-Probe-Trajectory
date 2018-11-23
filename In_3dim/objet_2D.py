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
		position (x, y): au
		vitesse (v_x, v_y) : au/day
	"""

	nom = "objet"
	masse = None
	x0 = 0
	y0 = 0
	vx0 = 0
	vy0 = 0
	#Listes des positions et vitesse 
	x = None 
	y = None
	vx = None
	vy = None 

	def __init__(self, nom = "objet", masse = None, x0 = 0, y0 = 0, vx0 = 0, vy0 = 0):
		"""Constructeur de notre classe"""
		self.nom = nom
		self.masse = masse
		self.x0 = x0
		self.y0 = y0
		self.vx0 = vx0
		self.vy0 = vy0


au = 1.49597870e11 #Unité astronomique
jour = 24*3600 #Un jour

G = 6.67408e-11 #Constante gravitationelle 


#Definition de fonction fx(M,x,y) et fy(M,x,y)
def fx(M,x,y):
	"""
	Retourne l'acceleration gravitationnelle suivant x dû à un objet de masse M distants de l'objet étudié de x**2+y**2
	"""
	return -((G*M)/(x**2+y**2)**(3/2))*x*(jour**2/au**3)

def fy(M,x,y):
	"""
	Retourne l'acceleration gravitationnelle suivant y dû à un objet de masse M distants de l'objet étudié de x**2+y**2
	"""
	return -((G*M)/(x**2+y**2)**(3/2))*y*(jour**2/au**3)

def E(M, x, y, vx, vy):
	"""
	Calculer l'energie massique d'un objet sous effet d'un seul objet de masse M
	"""
	return 0.5*(vx**2+vy**2)*(au**2/jour**2)-(G*M)/(np.sqrt(x**2+y**2)*au)
E = np.vectorize(E) #Vectoriser une fonction est benefique en terme de performance et memoire

def pot(M, x, y):
	"""
	Retourne le potentiel massique d'un objet par rapport à un autre objet de masse M et distant de x**2+y**2
	"""
	return -(G*M)/(np.sqrt(x**2+y**2)*au)

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

	ax = 0; ay = 0 #L'acceleration

	for ip in range(N):
		#Chaque objet bodies[ip] applique une force de gravitation sur l'objet bodies[i] 

		if ip == i: #On veut que pas avoir le même objet bodies[ip]
			continue
			
		ax += fx(bodies[ip].masse, bodies[i].x[j]-bodies[ip].x[j], bodies[i].y[j]-bodies[ip].y[j])
		ay += fy(bodies[ip].masse, bodies[i].x[j]-bodies[ip].x[j], bodies[i].y[j]-bodies[ip].y[j])

	return (ax, ay)

def Energy(bodies, i):

	"""
	L'Energie massique d'un objet sous l'effet d'autres objet qui lui entoure.
	"""

	N = len(bodies)

	potential = 0

	for ip in range(N):
		if ip == i:
			continue

		potential += pot(bodies[ip].masse, bodies[i].x-bodies[ip].x, bodies[i].y-bodies[ip].y)

	return 0.5*(au**2/jour**2)*(bodies[i].vx**2+bodies[i].vy**2)+potential

#[End]----------------------------------------------------------------------------------------------------	

