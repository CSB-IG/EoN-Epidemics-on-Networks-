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
        #El ciclo simplemente sirve para poder poder verificar las comunidades que se realizaron. 
    print(f"start_idx-{comunidades}")    
    return G, comunidades, P #Lo mas importante antes de realizar el algoritmo de gillespie es la G red, las comunidades que se crean y la matriz propabilidad P de conexiones.
  
#----------------------------------------------------------------------------------------------------
# Función que aplica la simulación Gillespie SIR
def aplicar_gillespie(G, tau, gamma, rho, t):
    sim = EoN.Gillespie_SIR(G, tau, gamma, rho=rho, tmax=t, return_full_data=True) #Esta parte ya fue aplicada y verifica en los anteriores algoritmos de redes dinamicas
    return sim # Con sim obtengo la simulacion con todos los parametros dados por el ususario asi que esta parte es importante. 
#Nota: El algoritmo de Gillespie_SIR puede ser cambiado por el fast_Gillespie solo se cambia el metodo que se quiere utilizar, lo demas se conserva igual y no afecta en proceso dinamico.

#----------------------------------------------------------------------------------------------------
# Función que muestra los nodos suseptibles, infectados y recuperados en t=i
def mostrar_estados(G, sim, i):
    susceptibles = [n for n in G.nodes() if sim.get_statuses(time=i)[n] == 'S'] #Este ciclo ayuda a poder tomar todos los individuos susceptibles
    infectados = [n for n in G.nodes() if sim.get_statuses(time=i)[n] == 'I'] #Este ciclo ayuda a poder tomar todos los individuos infectados
    recuperados = [n for n in G.nodes() if sim.get_statuses(time=i)[n] == 'R'] #Este ciclo ayuda a poder tomas todos los individuos recuperados
    print(f"Tiempo {i}: Susceptibles-{len(susceptibles)} Infectados-{len(infectados)} Recuperados-{len(recuperados)}") #Aqui mostramos la lista de individuos en cada tiempo i 
    return infectados, recuperados  #Solo se toman los valores que se actualizan en cada tiempo i, claro tambien los susceptibles pero no es necesario trabajar mas con ellos. 

def serie_temporal(sim,t):
    tiempos = range( t + 1 )
    S, I, R = [], [], [] #En esta parte generaremos listas vacias para garantizar la actualizacion de los estados en cada tiempo t y no repetir los datos en cada ciclo.
    for i in tiempos:
        estatus_tiempo = sim.get_statuses(time = i)# con get_statutes veremos el estado de los individuos en cada tiempo i para posteriormente extraer la informacion.
        # Con los siguientes comandos añadimos ya sean susptibles, infectados o recuperados segun sea la actualizacion de los datos generados por las funciones anteriores.
        S.append(sum(1 for e in estatus_tiempo.values() if e == 'S'))
        I.append(sum(1 for e in estatus_tiempo.values() if e == 'I'))
        R.append(sum(1 for e in estatus_tiempo.values() if e == 'R'))

    #Los siguientes comandos simplemente mostraran en pantalla la serie temporal de los estados de los invidviduos por suseptibles, infectados y recuperados.    
    plt.figure(figsize=(10, 6))
    plt.plot(tiempos, S, label="Saludables (S)", color='green')
    plt.plot(tiempos, I, label="Infectados (I)", color='red')
    plt.plot(tiempos, R, label="Recuperados (R)", color='blue')
    plt.xlabel("Tiempo")
    plt.ylabel("Número de individuos")
    plt.legend()
    plt.grid()
    plt.show()


#---------------------------------------------------------------------------------------------------
#Funcion principal la cual dependera de otras funciones para poder realizar la simulación dinamica SBM
def simular_sbm_dinamico(t, N, tau, gamma, kave, rho, numero_de_individuos, bloques,probabilidad_externa_base):
    # Colores llamativos para las comunidades
    colores_comunidades = ['#FF6347', '#FFD700', '#FF1493', '#00FFFF', '#32CD32', '#8A2BE2', '#FF4500', '#9ACD32', '#DA70D6', '#FF8C00']

    for z in range(1,N+1):
        #Las siguientes funciones ayudaran a tener un estandar para la simulacion la cual se trabajara hasta el N dado y en el tiempo i dado.
        G, comunidades, P = generar_red_SBM(kave, numero_de_individuos, bloques, probabilidad_externa_base)
        sim = aplicar_gillespie(G, tau, gamma, rho, t)

        for i in range(1, t+1):
            print(f"\n--- Tiempo {i} ---")
            infectados, recuperados = mostrar_estados(G, sim, i) #Invocando la funcion podemos ver los estados de los individuos ojo esta linea es muy importante.
            serie_temporal(sim, t) #Invocamos la funcion para ver la serie temporal, esta funcion puede ocuparse o no ya que solo muestra el estado de la simulacion graficamente, por lo tanto no existe problema si se elimina esta linea.
            

#----------------------------------------------------------------------------------------------------
# Parámetros de simulación
t = 10  # Duración de la simulación
N = 1  # Número de redes simuladas
gamma = 0.01  # Tasa de recuperación
rho = 0.2  # Fracción inicial de infectados
kave = 5  # Grado promedio de conexiones en la red
tau = 2 * gamma / kave  # Tasa de transmisión (Esta formula es parecida a la tasa de transmision de datos o información).
numero_de_individuos = 300  # Número de nodos
bloques = 8  # Número de comunidades
probabilidad_externa_base = 0.01 # Probabilidad base de conexión entre comunidades (puede variar entre pasos)



simular_sbm_dinamico(t, N, tau, gamma, kave, rho, numero_de_individuos, bloques,probabilidad_externa_base) # Ojo esta parte ayuda a invocar la funcion primordial,
#En caso de no tomar en cuenta esta informacion, el usuario es responsable del mal funcionamiento del sistema dinamico. 
