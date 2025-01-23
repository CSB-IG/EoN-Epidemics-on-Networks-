import networkx as nx
import EoN
import random
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------
# Función que genera la red usando el gráfico de Karate Club
def generar_red():
    G_i = nx.karate_club_graph()  # Usamos el gráfico predefinido del club de karate
    numero_de_individuos = len(G_i.nodes())  # Establecemos el número de nodos igual al tamaño de la red ya que tenemos que adaptar el 
    #algoritmo para ocupar karate_club y comprobar si el codigo es adecuado para n numeros de nodos 
    return G_i, numero_de_individuos

#----------------------------------------------------------------------------------------------------
# Función que aplica la simulación Gillespie SIR
def aplicar_gillespie(G, tau, gamma, rho, t):
    sim = EoN.Gillespie_SIR(G, tau, gamma, rho=rho, tmax=t, return_full_data=True)
    return sim

#----------------------------------------------------------------------------------------------------
# Función que muestra los nodos infectados y recuperados en t=i
def mostrar_estados(G, sim, i):
    susceptibles = [nodo for nodo in G.nodes() if sim.get_statuses(time=i)[nodo] == 'S']
    infectados = [nodo for nodo in G.nodes() if sim.get_statuses(time=i)[nodo] == 'I']
    recuperados = [nodo for nodo in G.nodes() if sim.get_statuses(time=i)[nodo] == 'R']
    print(f"En el tiempo {i}: Susceptibles - {susceptibles} Infectados - {infectados}, Recuperados - {recuperados}")
    return infectados, recuperados

#----------------------------------------------------------------------------------------------------
# Función que registra el estatus de los nodos en t=i
def registrar_estatus(sim, i):
    estatus_tiempo = sim.get_statuses(time=i)
    print(f"Estatus de los nodos en el tiempo {i}:")
    for nodo, estado in estatus_tiempo.items():
        print(f"Nodo {nodo}: {estado}")

#----------------------------------------------------------------------------------------------------
# Función que actualiza y muestra el árbol de transmisión
def actualizar_arbol_transmision(G, infectados, arbol_transmision, i):
    nuevos_infectados = set()
    for nodo in infectados:
        for vecino in G.neighbors(nodo):
            if vecino not in infectados:  # Asegurarse de que el vecino no está infectado
                nuevos_infectados.add(vecino)
                arbol_transmision.add_edge(nodo, vecino, tiempo=i)
    return nuevos_infectados

#----------------------------------------------------------------------------------------------------
# Función que genera y muestra la serie temporal de S, I, R
def serie_temporal(sim, t):
    tiempos = range(t + 1)
    S, I, R = [], [], []  # Listas para almacenar saludables, infectados y recuperados en cada tiempo
    
    for i in tiempos:
        estatus_tiempo = sim.get_statuses(time=i)
        s_count = sum(1 for estado in estatus_tiempo.values() if estado == 'S')
        i_count = sum(1 for estado in estatus_tiempo.values() if estado == 'I')
        r_count = sum(1 for estado in estatus_tiempo.values() if estado == 'R')
        S.append(s_count)
        I.append(i_count)
        R.append(r_count)

    # Graficar la serie temporal de S, I, R
    plt.figure(figsize=(10, 6))
    plt.plot(tiempos, S, label="Saludables (S)", color='green')
    plt.plot(tiempos, I, label="Infectados (I)", color='red')
    plt.plot(tiempos, R, label="Recuperados (R)", color='Aqua')
    plt.xlabel("Tiempo")
    plt.ylabel("Número de individuos")
    plt.title("Serie Temporal de Saludables, Infectados y Recuperados")
    plt.legend()
    plt.grid()
    plt.show()

#----------------------------------------------------------------------------------------------------
# Función principal que organiza la simulación y las visualizaciones
def generar_redes_transmision(t, tau, gamma, N, rho):
    for z in range(1, N + 1):
        G, numero_de_individuos = generar_red()  # Genera la red usando el gráfico Karate Club
        sim = aplicar_gillespie(G, tau, gamma, rho, t)  # Ejecuta la simulación
        arbol_transmision = nx.DiGraph()  # Grafo para el árbol de transmisión
    
        for i in range(1, t + 1):
            print(f"\n--- Tiempo {i} ---")
            print(f"Simulación de red número: {z}")
            # Mostrar los estados de los nodos en tiempo t=i
            infectados, recuperados = mostrar_estados(G, sim, i)
        
            # Actualizar el árbol de transmisión y obtener los nuevos infectados
            nuevos_infectados = actualizar_arbol_transmision(G, infectados, arbol_transmision, i)

            # Registrar el estatus de los nodos
            registrar_estatus(sim, i)
        
            # Graficar el árbol de transmisión
            pos = nx.spring_layout(arbol_transmision)
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111)

            # Asignar colores a los nodos en el árbol de transmisión
            color_map = []
            for nodo in arbol_transmision.nodes():
                if nodo in infectados:
                    color_map.append('red')  # Infectados en rojo
                elif nodo in recuperados:
                    color_map.append('Aqua')  # Recuperados en Aqua.
                else:
                    color_map.append('green')  # Otros nodos

            nx.draw(arbol_transmision, pos, ax=ax, with_labels=True, node_color=color_map, node_size=500, arrows=True)
            plt.title(f"Árbol de Transmisión hasta el tiempo {i}")
            plt.show()
            
            # Llamamos la función de serie temporal para ver el comportamiento en cada tiempo i
            serie_temporal(sim, i)

# Parámetros de simulación
t = 10  # Duración de la simulación
N = 1  # Número de redes a simular
gamma = 0.2  # Tasa de recuperación
rho = 0.1  # Fracción inicial de infectados
kave = 5  # Grado promedio de la red (no es necesario para el gráfico Karate Club)
tau = 0.1 # Tasa de transmisión (aún se usa, aunque el grado de la red es fijo)
# No necesitamos el parámetro numero_de_individuos, ya que el gráfico de Karate Club ya tiene este valor
#Tambien es importante saber que los valores de gamma, rho y tau no deberian tender a cero ya que el algoritmo no funciona 
#por el limite de nodos en nx.karate_club_graph()

# Llamado de la función principal para realizar la simulación
generar_redes_transmision(t, tau, gamma, N, rho)
