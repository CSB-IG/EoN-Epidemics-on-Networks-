import networkx as nx
import EoN
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from collections import defaultdict


print("Generacion de grafico G")
G = nx.grid_2d_graph(100,100) #cada nodo es (u,v) donde 0<=u,v<=99
#Inicialmente infectaremos a aquellos que estén cerca del medio
#El gráfico de cuadrícula tiene cada nodo conectado a sus cuatro vecinos más cercanos.
initial_infections = [(u,v) for (u,v) in G if 45<u<55 and 45<v<55]

H = nx.DiGraph() #Transiciones espontaneas
H.add_edge("Sus", "Vac", rate = 0.01)
H.add_edge("Inf", "Rec", rate = 1.0)

J = nx.DiGraph() #Transmiciones inducidas
J.add_edge(("Inf", "Sus"), ("Inf", "Inf"), rate = 2.0)

IC = defaultdict(lambda:"Sus") #un "dict", pero por defecto el valor es \texttt{’Sus’}.

for node in initial_infections:
	IC[node] = "Inf"

return_statuses = ["Sus", "Inf", "Rec", "Vac"]

color_dict = {"Sus": "#009a80","Inf":"#ff2000", "Rec":"gray","Vac": "#5AB3E6"}
pos = {node:node for node in G}
tex = False
sim_kwargs = {"color_dict":color_dict, "pos":pos, "tex":tex}


print("Haciendo simulación de Gillespie")
sim = EoN.Gillespie_simple_contagion(G, H, J, IC, return_statuses, tmax=30, return_full_data=True, sim_kwargs=sim_kwargs)
times, D = sim.summary()
#
#times es una matriz numpy de horas. D es un diccionario, cuyas claves son las entradas en
#return_status. Los valores son matrices numpy que dan el número en ese
#status en el momento correspondiente.
newD = {"Sus+Vac":D["Sus"]+D["Vac"], "Inf+Rec" : D["Inf"] + D["Rec"]}
#
#newD es un nuevo diccionario que proporciona el número de personas que aún no han sido infectadas o el número de personas que alguna vez fueron infectadas
#Agreguemos esta serie temporal a la simulación.
#
new_timeseries = (times, newD)
sim.add_timeseries(new_timeseries, label = "Simulation", color_dict={"Sus+Vac":"#E69A00", "Inf+Rec":"#CD9AB3"})

sim.display(time=6, node_size = 4, ts_plots=[["Inf"], ["Sus+Vac", "Inf+Rec"]])
plt.show()

#Esta parte solamente es para mostrar una simulacion en tiempo real y ver como se comporta el modelo. 

#ani=sim.animate(ts_plots=[["Inf"], ["Sus+Vac", "Inf+Rec"]], node_size = 4)
#ani.save("SIRV_animate.mp4", fps=5, extra_args=["-vcodec", "libx264"])
