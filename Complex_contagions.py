import networkx as nx
import EoN
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def transition_rate(G, node, status, parameters):

	#Esta función debe devolver la tasa a la que \texttt{node} cambia de estado.
	#Para el modelo que estamos asumiendo, debería devolver 1 si \texttt{node} tiene al menos
	#socios infectados y 0 en caso contrario. La información sobre el umbral
	#se proporciona en la tupla \texttt{parameters}.

	r = parameters[0] #El umbral

	#Si hay parejas susceptibles y al menos \texttt{r} infectadas, entonces la tasa es 1
	if status[node] == "S" and len([nbr for nbr in G.neighbors(node) if #G.neighbors evuelve un iterador sobre todos los vecinos del nodo n.
											status[nbr] == "I"])>=r:
		return 1
	else:
		return 0

def transition_choice(G, node, status, parameters):

	#Esta función debe devolver el nuevo estado del nodo. Suponemos que al entrar
	#ya hemos calculado que está cambiando de estado.
	#Esta función podría ser más elaborada si hubiera diferentes
	#transiciones posibles que pudieran ocurrir. Sin embargo, para este modelo,
	#los nodos 'I' no están cambiando de estado, y los 'S' están cambiando a
	#'I'. Entonces, si estamos en esta función, el nodo debe ser 'S' y convertirse en 'I'

	return "I"

def get_influence_set(G, node, status, parameters):

	#Esta función debe devolver un conjunto que contenga todos los nodos cuyas tasas
	#podrían cambiar debido a que \texttt{node} acaba de cambiar de estado. Es decir, ¿qué nodos
	#podrían verse afectados por \texttt{node}?
	#Para nuestros modelos, los únicos nodos a los que un nodo podría afectar son los vecinos susceptibles.

	return {nbr for nbr in G.neighbors(node) if status[nbr] == "S"}


parameters = (2,)
#este es el umbral. Tenga en cuenta la coma. Es necesaria
#para que Python se dé cuenta de que se trata de una tupla de 1, no solo un
#número.\texttt{parámetros} se envía como una tupla, por lo que necesitamos
#la coma.
N = 600000
deg_dist = [2, 4, 6]*int(N/3) #int pasa un valor real a el entero inferior proximo.
print("generando gráfico G con {} nodos".format(N))
G = nx.configuration_model(deg_dist)# Devuelve un gráfico aleatorio con la secuencia de grados dada.

for rho in np.linspace(3./80, 7./80, 8): #Devuelve números espaciados uniformemente durante un intervalo específico.
	#8 valores de 3/80 a 7/80.
	print(rho)
	IC = defaultdict(lambda: "S")

	for node in G.nodes():
		if np.random.random()<rho: #there are faster ways to do this random
		#selection
			IC[node] = "I"
	
	print("Simulación de Gillespie")
	t, S, I = EoN.Gillespie_complex_contagion(G, transition_rate,
											transition_choice, get_influence_set, IC,
											return_statuses = ("S", "I"),
											parameters = parameters) # Simulacón compleja de Gillespie
	print("Terminé con la simulación, ahora estoy trazando")
	plt.plot(t, I)



plt.xlabel("$t$")
plt.ylabel("Numero de infectados")
plt.show()
