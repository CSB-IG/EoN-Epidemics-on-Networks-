import networkx as nx
import EoN
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------
# Función que genera la red
def generar_red():
    G=nx.karate_club_graph()  # Genera la red de club de karate con 34 nodos 
    return G

#----------------------------------------------------------------------------------------------------
# Función que aplica la simulación Gillespie SIR
def aplicar_gillespie(G, tau, gamma, t):
    sim=EoN.Gillespie_SIR(G, tau, gamma, tmax=t, return_full_data=True)
    return sim

#----------------------------------------------------------------------------------------------------
# Función que muestra los nodos infectados y recuperados en t=i
def mostrar_estados(G, sim, i):
    infectados=[nodo for nodo in G.nodes() if sim.get_statuses(time=i)[nodo] == 'I']
    recuperados=[nodo for nodo in G.nodes() if sim.get_statuses(time=i)[nodo] == 'R']
    print(f"En el tiempo {i}: Infectados - {infectados}, Recuperados - {recuperados}")
    return infectados, recuperados

#----------------------------------------------------------------------------------------------------
# Función que registra el estatus de los nodos en t=i
def registrar_estatus(sim, i):
    estatus_tiempo=sim.get_statuses(time=i)
    print(f"Estatus de los nodos en el tiempo {i}:")
    for nodo, estado in estatus_tiempo.items():
        print(f"Nodo {nodo}: {estado}")

#----------------------------------------------------------------------------------------------------
# Función que actualiza y muestra el árbol de transmisión
def actualizar_arbol_transmision(G, infectados, arbol_transmision, i):
    nuevos_infectados=set()
    for nodo in infectados:
        for vecino in G.neighbors(nodo):
            if vecino not in infectados:  # Asegurarse de que el vecino no está infectado
                nuevos_infectados.add(vecino)
                arbol_transmision.add_edge(nodo, vecino, tiempo=i)
    print(f"Posibles infectados y recuperados en el tiempo {i}: {nuevos_infectados}")
    return nuevos_infectados

#----------------------------------------------------------------------------------------------------
# Función principal que organiza la simulación y las visualizaciones
def unir_redes(t, tau, gamma):
    G = generar_red()  # Genera la red
    sim = aplicar_gillespie(G, tau, gamma, t)  # Ejecuta la simulación
    arbol_transmision=nx.DiGraph()  # Grafo para el árbol de transmisión

    for i in range(1,t+1):
        print(f"\n--- Tiempo {i} ---")

        # Mostrar los estados de los nodos en tiempo t=i
        infectados, recuperados=mostrar_estados(G, sim, i)
        
        
        # Actualizar el árbol de transmisión y obtener los nuevos infectados
        nuevos_infectados=actualizar_arbol_transmision(G, infectados, arbol_transmision, i)

        # Registrar el estatus de los nodos
        registrar_estatus(sim, i)
        
        # Graficar el árbol de transmisión
        pos=nx.spring_layout(arbol_transmision)

        # Asignar colores a los nodos en el árbol de transmisión
        color_map=[]
        for nodo in arbol_transmision.nodes():
            if nodo in infectados:
                color_map.append('orange')  # Infectados en naranja
            elif nodo in recuperados:
                color_map.append('green')  # Recuperados en verde
            else:
                color_map.append('lightblue')  # Otros nodos

        nx.draw(arbol_transmision, pos, with_labels=True, node_color=color_map, node_size=500, arrows=True)
        plt.title(f"Árbol de Transmisión hasta el tiempo {i}")
        plt.show()


#.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.

#Aqui simplemente metemos los datos y obtendremos los resultados deseados como 
#los infectados, recuperados y posibles infectados y recuperados
#Como una tabla que muestra los estados de los nodos en cada tiempo i
#(Recordar que la red generada es de un maximo de 34 individuos, mas adelante se presentara una forma de generar N individuos solo agregando
#un numero y posiblemente mas datos).

# Parámetros de simulación
t=5  # Duración de la simulación
tau=0.2  # Tasa de transmisión
gamma=0.1  # Tasa de recuperación

unir_redes(t, tau, gamma)

#M4uroCube.
 
