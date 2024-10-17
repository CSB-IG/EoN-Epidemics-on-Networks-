import networkx as nx
import EoN
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------------------------------------
# Función que genera la red
def generar_red():
    G = nx.karate_club_graph()  # Genera la red de club de karate de 34 nodos 
    return G

#--------------------------------------------------------------------------------------------------------
# Función que aplica la simulación Gillespie SIR
def aplicar_gillespie(G, tau, gamma, t):
    sim = EoN.Gillespie_SIR(G, tau, gamma, tmax=t, return_full_data=True)  # Ejecuta la simulación del modelo 
    #Gillespie con los nodos que creamos, los infectados iniciales y la taza de transmición.
    return sim

#------------------------------------------------------------------------------------------------------------
# Función que muestra solo los nodos infectados en t=i
def mostrar_estados(G, sim, i):
    infectados = [nodo for nodo in G.nodes() if sim.get_statuses(time=i)[nodo] == 'I'] #get_statuses recuperamos la información necesaria 
    #Para ver el estatus de los nodos en cada tiempo i.
    print(f"En el tiempo {i}: Infectados - {infectados}")
    #Aqui paso por cada nodo generado y solo extraigo los nodos infectados 
    return infectados

#------------------------------------------------------------------------------------------------------
# Función que registra el estatus de los nodos infectados en t=i
def registrar_estatus(sim, i):
    estatus_tiempo = sim.get_statuses(time=i)
    print(f"Estados de los nodos{i}:")
    for nodo, estado in estatus_tiempo.items():
        print(f"Nodo {nodo}: {estado}")
        #Con esta funcion voy a mostrar la lista de nodos que infectaron a otros en cada tiempo i.

#-------------------------------------------------------------------------------------------------
# Función que actualiza y muestra el árbol de transmisión
def actualizar_arbol_transmision(G, infectados, arbol_transmision, i):
    nuevos_infectados = set() #Almacenamos datos de nuevos infectados.
    for nodo in infectados:
        for vecino in G.neighbors(nodo): #trata de buscar los K puntos más cercanos a un punto concreto para poder inferir su valor es decir si el vecino esta infectado o no. 
            if vecino not in infectados:  # Asegurarse de que el vecino no está infectado
                nuevos_infectados.add(vecino)#add ayudara solo a extraer los vecinos infectados 
                arbol_transmision.add_edge(nodo, vecino, tiempo=i)#Estraemos la dupla de nodos y vecino para crear un borde. 
    print(f"Posibles infectados por interaccionen el tiempo {i}: {nuevos_infectados}")
    return nuevos_infectados
    #Con esta funcion se muestran los nodos que se infectaron por interacción. y posibles infecciosos.

#------------------------------------------------------------------------------------------------------
# Función principal que organiza la simulación y las visualizaciones
def unir_redes(t, tau, gamma):
    G = generar_red()  # Genera la red
    sim = aplicar_gillespie(G, tau, gamma, t)  # Ejecuta la simulación
    arbol_transmision = nx.DiGraph()  # Gráfico para el árbol de transmisión

    for i in range(1, t + 1):
        print(f"\n--- Tiempo {i} ---")

        # Mostrar los estados de los nodos en tiempo t=i
        infectados = mostrar_estados(G, sim, i)
        
        
        # Actualizar el árbol de transmisión y obtener los nuevos infectados
        nuevos_infectados = actualizar_arbol_transmision(G, infectados, arbol_transmision, i)

        # Registrar el estatus de los nodos infectados
        registrar_estatus(sim, i)
        
        # Graficar el árbol de transmisión
        pos = nx.spring_layout(arbol_transmision) #El algoritmo simula una representación de la red dirigida por la fuerza los bordes 
        nx.draw(arbol_transmision, pos, with_labels=True, node_color='lightblue', node_size=500, arrows=True)
        plt.title(f"Árbol de Transmisión hasta el tiempo {i}")
        plt.show()

# Parámetros de simulación
t = 3  # Duración de la simulación
tau = 0.2  # Tasa de transmisión
gamma = 0  # Tasa de recuperación

unir_redes(t, tau, gamma)
