import networkx as nx
import EoN
import random
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle


#---------------------------------------------------------------------------------------------------
def generar_red_SBM(kave, numero_de_individuos, bloques, probabilidad_externa_base):
    #tam sera el tamaño que tendran nuestras comunidades 
    tam = [numero_de_individuos // bloques] * bloques #Aqui hacemos una division dada por el usuario de bloques, y se asigna el numero total de individuos en cada bloque, ojo aqui puede no encluir todavia a todo el conjunto de los individuos dados
    for i in range(numero_de_individuos % bloques):  
        tam[i] += 1 # Con este ciclo en caso de que falten individuos por meter en los bloques entonces lo que se hace es terminar de añadirlos.                           

    # Probabilidad de conexión dentro de la misma comunidad
    probabilidad_interna = kave / (numero_de_individuos - 1)
    

    # Construcción de la matriz de probabilidades (P)
    P = np.full((bloques, bloques), probabilidad_externa_base)
    np.fill_diagonal(P, probabilidad_interna)

     #Se crea la red se SBM
    G = nx.stochastic_block_model(tam, P)

    
    comunidades = []
    start_idx = 0
    #En esta parte se utiliza para determinar cuántos nodos pertenecen a cada comunidad y para generar los conjuntos de nodos que se almacenan en comunidades
    for size in tam:
        comunidades.append(set(range(start_idx, start_idx + size)))
        start_idx += size

    print(f"start_idx-{comunidades}")    
    return G, comunidades, P
  
#----------------------------------------------------------------------------------------------------
# Función que aplica la simulación Gillespie SIR
def aplicar_gillespie(G, tau, gamma, rho, t):
    sim = EoN.Gillespie_SIR(G, tau, gamma, rho=rho, tmax=t, return_full_data=True) #Esta parte ya fue aplicada y verifica en los anteriores algoritmos de redes dinamicas
    return sim

#----------------------------------------------------------------------------------------------------
# Función que muestra los nodos suseptibles, infectados y recuperados en t=i
def mostrar_estados(G, sim, i):
    susceptibles = [n for n in G.nodes() if sim.get_statuses(time=i)[n] == 'S']
    infectados = [n for n in G.nodes() if sim.get_statuses(time=i)[n] == 'I']
    recuperados = [n for n in G.nodes() if sim.get_statuses(time=i)[n] == 'R']
    print(f"Tiempo {i}: Susceptibles-{len(susceptibles)} Infectados-{len(infectados)} Recuperados-{len(recuperados)}")
    return infectados, recuperados

#---------------------------------------------------------------------------------------------------
#Funcion principal la cual dependera de otras funciones para poder realizar la simulación dinamica SBM
def simular_sbm_dinamico(t, N, tau, gamma, kave, rho, numero_de_individuos, bloques,probabilidad_externa_base):
    # Colores llamativos para las comunidades
    colores_comunidades = ['#FF6347', '#FFD700', '#FF1493', '#00FFFF', '#32CD32', '#8A2BE2', '#FF4500', '#9ACD32', '#DA70D6', '#FF8C00']

    for z in range(1,N+1):
        G, comunidades, P = generar_red_SBM(kave, numero_de_individuos, bloques, probabilidad_externa_base)
        sim = aplicar_gillespie(G, tau, gamma, rho, t)

        for i in range(1, t+1):
            print(f"\n--- Tiempo {i} ---")
            infectados, recuperados = mostrar_estados(G, sim, i)

#----------------------------------------------------------------------------------------------------
# Parámetros de simulación
t = 10  # Duración de la simulación
N = 1  # Número de redes simuladas
gamma = 0.1  # Tasa de recuperación
rho = 0.1  # Fracción inicial de infectados
kave = 5  # Grado promedio de conexiones en la red
tau = 2 * gamma / kave  # Tasa de transmisión
numero_de_individuos = 300  # Número de nodos
bloques = 8  # Número de comunidades
probabilidad_externa_base = 0.01 # Probabilidad base de conexión entre comunidades (puede variar entre pasos)



simular_sbm_dinamico(t, N, tau, gamma, kave, rho, numero_de_individuos, bloques,probabilidad_externa_base)
