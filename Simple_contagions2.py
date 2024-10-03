import EoN
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt


N = 300000

print("generando gráfico G con {} nodos".format(N))
G = nx.fast_gnp_random_graph(N, 5./(N-1))
#En lo que sigue:
#’SS’ significa un individuo susceptible a ambas enfermedades
#’SI’ significa susceptible a la enfermedad 1 e infectado con la enfermedad 2
#’RS’ significa recuperado de la enfermedad 1 y susceptible a la enfermedad 2.
#etc.
H = nx.DiGraph()# Crea una estructura de gráfico vacía (un “gráfico nulo”) sin nodos ni aristas.
#DiGraph que muestra transiciones espontáneas
#(no se requieren interacciones entre individuos)

H.add_node("SS")#En realidad no necesitamos incluir el nodo 'SS' en H.
H.add_edge("SI", "SR", rate = 1) #Un individuo que es susceptible a la enfermedad
#1 e infectado con la enfermedad 2 se recuperará
#de la enfermedad 2 con una tasa de 1.
H.add_edge("IS", "RS", rate = 1)
H.add_edge("II", "IR", rate = 0.5)
H.add_edge("II", "RI", rate = 0.5)
H.add_edge("IR", "RR", rate = 0.5)
H.add_edge("RI", "RR", rate = 0.5)
#En la parte inferior, el borde ((’SI’, ’SS’), (’SI’, ’SI’)) significa que un
#individuo ‘SI’ conectado a un individuo ‘SS’ puede conducir a una transición en
#la cual el individuo ‘SS’ se convierte en ‘SI’. La tasa de esta transición es 0,18.
#
#Tenga en cuenta que los individuos \texttt{IR} y \texttt{RI} son más infecciosos que otros
#individuos.
#
J = nx.DiGraph()
#DiGraph que muestra transiciones inducidas (requiere interacción).

J.add_edge(("SI", "SS"), ("SI", "SI"), rate = 0.18)
J.add_edge(("SI", "IS"), ("SI", "II"), rate = 0.18)
J.add_edge(("SI", "RS"), ("SI", "RI"), rate = 0.18)
J.add_edge(("II", "SS"), ("II", "SI"), rate = 0.18)
J.add_edge(("II", "IS"), ("II", "II"), rate = 0.18)
J.add_edge(("II", "RS"), ("II", "RI"), rate = 0.18)
J.add_edge(("RI", "SS"), ("RI", "SI"), rate = 1)
J.add_edge(("RI", "IS"), ("RI", "II"), rate = 1)
J.add_edge(("RI", "RS"), ("RI", "RI"), rate = 1)
J.add_edge(("IS", "SS"), ("IS", "IS"), rate = 0.18)
J.add_edge(("IS", "SI"), ("IS", "II"), rate = 0.18)
J.add_edge(("IS", "SR"), ("IS", "IR"), rate = 0.18)
J.add_edge(("II", "SS"), ("II", "IS"), rate = 0.18)
J.add_edge(("II", "SI"), ("II", "II"), rate = 0.18)
J.add_edge(("II", "SR"), ("II", "IR"), rate = 0.18)
J.add_edge(("IR", "SS"), ("IR", "IS"), rate = 1)
J.add_edge(("IR", "SI"), ("IR", "II"), rate = 1)
J.add_edge(("IR", "SR"), ("IR", "IR"), rate = 1)


return_statuses = ("SS", "SI", "SR", "IS", "II", "IR", "RS", "RI", "RR")

initial_size = 250
IC = defaultdict(lambda: "SS")


for individual in range(initial_size):
	#comienza con algunas personas que tienen ambas
	IC[individual] = "II"

for individual in range(initial_size, 5*initial_size): #and more with only
	#la segunda enfermedad
	IC[individual] = "SI"


print("Simulación de Gillespie")
t, SS, SI, SR, IS, II, IR, RS, RI, RR = EoN.Gillespie_simple_contagion(G, H,J, IC, return_statuses,tmax = float("Inf"))

plt.semilogy(t, IS+II+IR, "-.", label = "Infected with disease 1")
plt.semilogy(t, SI+II+RI, "-.", label = "Infected with disease 2")
plt.xlabel("$t$")
plt.ylabel("Numero de infectados")
plt.legend()
plt.show()
