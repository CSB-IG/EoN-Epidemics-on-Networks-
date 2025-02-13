import networkx as nx
import EoN
import random
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------
# Función que genera la red
def generar_red(kave, numero_de_individuos):
    # Ajustar infec_ratio para obtener el grado promedio kave
    infec_ratio = kave / (numero_de_individuos - 1)
    G_i = nx.fast_gnp_random_graph(numero_de_individuos, infec_ratio)  # Crear red con N nodos y grado promedio kave

    return G_i  # Retornar la red generada

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
    print(f"Tiempo {i}:Susceptibles - {susceptibles} Infectados - {infectados}, Recuperados - {recuperados}")
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

    return nuevos_infectados

#----------------------------------------------------------------------------------------------------
# Serie temporal de Saludables, infectados y Recuperados.
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

#------------------------------------------------------------------------------------------------------------------------------------------------
# Función principal que organiza la simulación y las visualizaciones
def generar_redes_transmision(t, tau, gamma, N, kave, rho, numero_de_individuos):
    for z in range(1, N + 1):
        G = generar_red(kave, numero_de_individuos)  # Genera la red con grado promedio kave
        sim = aplicar_gillespie(G, tau, gamma, rho, t)  # Ejecuta la simulación
        arbol_transmision = nx.DiGraph()  # Grafo para el árbol de transmisión
    
        for i in range(1, t + 1):
            print(f"\n--- Tiempo {i} ---")
            print(f"simulación de red numero:{z} ")
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
            plt.title(f"Árbol de Transmisión en el tiempo {i}")
            plt.show()
            
            # Llamamos la función de serie temporal para ver el comportamiento en cada tiempo i
            serie_temporal(sim, i)


#--------------------------------------------------------------------------------------------------------------------------------------------
# Parámetros de simulación
t = 10  # Duración de la simulación.
N = 1  # Número de redes que se quieren simular, se muestra una red primero y despues una nueva red, cada una diferente y pueden ser varias.
#---------------------------------------------------------------------------------------------------------------------------------------------------
gamma = 0.1  # Tasa de recuperación. L = 1/gamma o donde L es la tasa de recuperación en caso de no saber como calcular L simplemente es el promedio.
# de el tiempo que tarda en recuperarse cada persona entre el numero de personas, L= suma de dias de cada individuo para recuperarse/'n' numero de personas. Gamma simplemente se
#calcula despejando la misma variable gamma de la ecuación.
#---------------------------------------------------------------------------------------------------------------------------------------------------
rho = 0.01  # fraccion inicial de nodos infectados. Los valores deben de estar entre 0<=rho<=1 ya que 0 representa el 0% de nodos iniciales infectados
# y 1 representa el 100% de los nodos infectados. 
#---------------------------------------------------------------------------------------------------------------------------------------------------
kave = 5  # Grado promedio de conexiones en la red.
tau = 2 * gamma / kave # Tasa de transmisión. (Esta formula es parecida a la tasa de transmision de datos o información).
numero_de_individuos = 200
  #Numero de individuos que se tendra en la poblacion a simular. 

#--------------------------------------------------------------------------------------------------------------------------------------------------
#Llamado de la funcion la cual tiene como objetivo realizar toda la simulacion solo agregando parametros 
generar_redes_transmision(t, tau, gamma, N, kave, rho, numero_de_individuos)

#Como se puede observar el codigo es muy parecido al algoritmo sim_red_dim_SIR.py (Se encuentra en el repositorio de GitHub) ya que el objetivo era trabajar mientras se generalizaba 
#el proceso, para generar una red dinamica adecuada y reutilizable en el momento que sea necesario. 
#Por eso mismo la generacion de funciones, para simplemente poder ensamblar partes del codigo y tener los calculos, 
#datos y herramientas para futuros proyectos. Quien logre poner antecion en los comentarios de este codigo recuerden que
#este codigo me llevo horas extra de servicio social en el INMEGEN y bastante tiempo de analisis. (Echo por Jesús Mauricio Flores de Modelación Matemática SLT UACM)

#M4uroCube.
