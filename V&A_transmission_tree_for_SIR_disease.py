import networkx as nx
import EoN
import matplotlib.pyplot as plt



G = nx.karate_club_graph()

nx_kwargs = {"with_labels":True} #argumentos opcionales que se pasarán al comando de trazado 
#networkx.

print("Haciendo simulación de Gillespie")
sim = EoN.Gillespie_SIR(G, 1, 1, return_full_data=True)
print("Terminé con la simulación, ahora estoy trazando")

sim.display(time=1) #Esto produce una instantánea (estocástica) en el momento 1:
#Al parecer tengo un problema particular para agregar las etiquetas el pasar el siguiente comando ,**nx_kwargs
#Encaso de querer utilizarlo solo quite el comentario de la siguiente linea y comente la linea anterior:
# sim.display(time=1,**nx_kwargs)
plt.show()

T = sim.transmission_tree() #Un DiGraph de networkx con el árbol de transmisión
Tpos = EoN.hierarchy_pos(T) #pos para un gráfico de networkx

fig = plt.figure(figsize = (8,5))
ax = fig.add_subplot(111)
nx.draw(T, Tpos, ax=ax, node_size = 200, with_labels=True)
plt.show()
