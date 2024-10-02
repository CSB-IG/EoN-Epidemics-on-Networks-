import networkx as nx
import EoN
import matplotlib.pyplot as plt
import numpy as np

def rec_time_fxn_gamma(u):
	return np.random.gamma(3,0.5) #numero aleatorio con distribucion gamma

def trans_time_fxn(u, v, tau):
	if tau >0:
		return np.random.exponential(1./tau) #Extraer muestras de una distribución exponencial.
	else:
		return float("Inf")

N = 10**6 #numero de individuos 
kave = 5
#Numero esperado de compañeros infectados

print("generando gráfico G con {} nodos".format(N))
G = nx.fast_gnp_random_graph(N, kave/(N-1)) #Erdo’’s-Re’nyi, Devuelve un
#Gráfico aleatorio, también conocido como gráfico de Erdős-Rényi o gráfico binomial.
tau = 0.3


for cntr in range(10):
	print(cntr)
	print("Realizar simulación basada en eventos")
	t, S, I, R = EoN.fast_nonMarkov_SIR(G, trans_time_fxn = trans_time_fxn,
																rec_time_fxn = rec_time_fxn_gamma,
																trans_time_args = (tau,))
#Para reducir el tamaño del archivo y hacer que el trazado sea más rápido, simplemente trazaremos 1000
#puntos de datos. En realidad, no es necesario aquí, pero esto demuestra
#una de las herramientas disponibles en EoN.

	subsampled_ts = np.linspace(t[0], t[-1], 1000) # Devuelve números espaciados uniformemente durante un intervalo específico.
	subI, subR = EoN.subsample(subsampled_ts, t, I, R)
	#Dada una lista/matriz de horarios para informar, 
	#devuelve la cantidad de nodos de cada estado en esos horarios.los devuelve
    #submuestreados en momentos de informe específicos. 
	print("Terminé con la simulación, ahora estoy trazando")
	plt.plot(subsampled_ts, subI+subR)


	
plt.xlabel("$t$")
plt.ylabel("Número infectado o recuperado")
plt.show()
