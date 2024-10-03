import EoN
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
import random
N = 100000
print("generando gráfico G con {} nodos".format(N))
G = nx.fast_gnp_random_graph(N, 5./(N-1))# Devuelve un Gráfico aleatorio, también conocido como gráfico de Erdős-Rényi o gráfico binomial.
#Añadimos variación aleatoria en la tasa de abandono de la clase expuesta
#y en la tasa de transmisión de la asociación.
#No hay variación en la tasa de recuperación.
node_attribute_dict = {node: 0.5+random.random() for node in G.nodes()}
edge_attribute_dict = {edge: 0.5+random.random() for edge in G.edges()}
nx.set_node_attributes(G, values=node_attribute_dict,
name="expose2infect_weight")
nx.set_edge_attributes(G, values=edge_attribute_dict,
name="transmission_weight")
#
#Estos atributos individuales y de asociación se utilizarán para escalar
#las tasas de transición. Cuando definimos \texttt{H} y \texttt{J}, proporcionamos el nombre
#de estos atributos.

#Se muestran técnicas más avanzadas para escalar las tasas de transmisión en
#la documentación en línea
H = nx.DiGraph() #Para las transiciones espontáneas
H.add_node("S") #Esta línea en realidad es innecesaria.
H.add_edge("E", "I", rate = 0.6, weight_label="expose2infect_weight")
H.add_edge("I", "R", rate = 0.1)
J = nx.DiGraph() #para las transiciones inducidas
J.add_edge(("I", "S"), ("I", "E"), rate = 0.1,
weight_label="transmission_weight")
IC = defaultdict(lambda: "S")

for node in range(200):
	IC[node] = "I"

return_statuses = ("S", "E", "I", "R")

print("Simulación de Gillespie")
t, S, E, I, R = EoN.Gillespie_simple_contagion(G, H, J, IC, return_statuses,
tmax = float("Inf"))#Simulación de Gillespie para contagio simple.

print("Terminé con la simulación, ahora estoy trazando")
plt.plot(t, S, label = "Suseptible")
plt.plot(t, E, label = "Expuesto")
plt.plot(t, I, label = "Infectado")
plt.plot(t, R, label = "Recuperado")
plt.xlabel("$t$")
plt.ylabel("Numeros simulados")
plt.legend()
plt.show()
