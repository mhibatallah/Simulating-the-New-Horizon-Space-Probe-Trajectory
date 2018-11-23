	#Definition de pas de temps
	dt = 1 #step
	T = int(365/dt)*10 # (Nombre de steps)<-> Periode d'integration T = int(365/dt)* nbr ans

def implementation(bodies, dt, T):
	#Intialisation des attributs x,y,z,vx,vy,vz de chaque objet bodies[i]
	for i in range(Nbr_obj):
		bodies[i].x = np.zeros(T); bodies[i].x[0] = bodies[i].x0
		bodies[i].y = np.zeros(T); bodies[i].y[0] = bodies[i].y0
		bodies[i].z = np.zeros(T); bodies[i].z[0] = bodies[i].z0

		bodies[i].vx = np.zeros(T); bodies[i].vx[0] = bodies[i].vx0
		bodies[i].vy = np.zeros(T); bodies[i].vy[0] = bodies[i].vy0
		bodies[i].vz = np.zeros(T); bodies[i].vz[0] = bodies[i].vz0

	#Definitions des v_demi.
	vx_demi = np.zeros(Nbr_obj)
	vy_demi = np.zeros(Nbr_obj)
	vz_demi = np.zeros(Nbr_obj)

	#Implementation de l'integrateur de Verlet pour chaque objet (sauf le soleil)
	for j in range(T-1): 

	#Phase 1: Calcul de vitesses milieu et affectation des position a l'intant j+1
		for i in range(1,Nbr_obj): #Modification des parametres pour chaque objet a l' instant j

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

	    #Phase 2: Affectation des vitesse a l'instant j+1   
		for i in range(1,Nbr_obj):

			#L'acceleration au pas i+1 relative à l'objet j
			fx_jplus1, fy_jplus1, fz_jplus1 = acceleration_sol(bodies, i, j+1) #Il faut faire cette étape après le calcul de postion à l'indice i+1

	        # Affectation des vitesses à l'indice j+1
			bodies[i].vx[j+1] = vx_demi[i] + (dt/2)*fx_jplus1
			bodies[i].vy[j+1] = vy_demi[i] + (dt/2)*fy_jplus1
			bodies[i].vz[j+1] = vz_demi[i] + (dt/2)*fz_jplus1

	#[End]----------------------------------------------------------------------------------------------------