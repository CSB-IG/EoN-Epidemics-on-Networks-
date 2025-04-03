import networkx as nx # para crear y manipular la red.
import EoN # para simular la propagación de la epidemia.
import random # para asignar estados iniciales aleatorios.
import numpy as np #  para manejar datos numéricos y realizar cálculos.
import matplotlib.pyplot as plt # para visualizar la red y la evolución de la epidemia.
from itertools import cycle #  para asignar colores o estilos de manera cíclica en la visualización.


#---------------------------------------------------------------------------------------------------
def generar_red_SBM(kave, numero_de_individuos, bloques, probabilidad_externa_base):
    #tam sera el tamaño que tendran nuestras comunidades 
    tam = [numero_de_individuos // bloques] * bloques #Aqui hacemos una division dada por el usuario de bloques, y se asigna el numero total de individuos en cada bloque, ojo aqui puede no encluir todavia a todo el conjunto de los individuos dados
    for i in range(numero_de_individuos % bloques):  
        tam[i] += 1 # Con este ciclo en caso de que falten individuos por meter en los bloques entonces lo que se hace es terminar de añadirlos.                           

    # Asegurar que la probabilidad interna no exceda 1 (para redes muy densas)
    probabilidad_interna = min(kave / (numero_de_individuos - 1), 1.0)
    

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


#----------------------------------------------------------------------------------------------------
# Función para visualizar una red SBM (Stochastic Block Model) con estados epidémicos
def visualizar_red_sbm(G, sim, i, comunidades, colores_comunidades, titulo="Red SBM"):
    # Obtener el estado actual ('S', 'I' o 'R') de cada nodo en el tiempo i
    estados = sim.get_statuses(time=i)  
    
    # Asignar colores a nodos según su estado epidemiológico:
    # - Verde ('green') para Susceptibles ('S')
    # - Rojo ('red') para Infectados ('I')
    # - Azul ('blue') para Recuperados ('R')
    # A cada nodo se le podra asignar los colores que se desean para poder tener una visualizacion mas dinamica. 
    color_nodos = []
    for nodo in G.nodes():
        if estados[nodo] == 'S':
            color_nodos.append('green')
        elif estados[nodo] == 'I':
            color_nodos.append('red')
        elif estados[nodo] == 'R':
            color_nodos.append('blue')
    
    # Asignar colores fijos a las comunidades (cada comunidad mantiene su color)
    color_comunidad = []
    for nodo in G.nodes():
        for idx, comunidad in enumerate(comunidades):
            if nodo in comunidad:
                # Usa colores cíclicamente si hay más comunidades que colores definidos
                color_comunidad.append(colores_comunidades[idx % len(colores_comunidades)])
                break
    
    # Crear disposición espacial de nodos (layout) agrupando por comunidades
    pos = {}  # Diccionario para almacenar posiciones {nodo: (x,y)}
    offset_x = 0  # Desplazamiento horizontal entre comunidades
    
    for comunidad in comunidades:
        # Extraer subgrafo de la comunidad actual
        comunidad_G = G.subgraph(comunidad)  
        # Calcular disposición en círculo para esta comunidad (semilla fija para reproducibilidad)
        comunidad_pos = nx.spring_layout(comunidad_G, seed=42)  
        
        # Ajustar coordenadas para separar comunidades horizontalmente
        for nodo, p in comunidad_pos.items():
            pos[nodo] = (p[0] + offset_x, p[1])  # Desplaza en eje X
        
        offset_x += 3  # Aumentar el espacio entre comunidades este puede cambiar segun la neceidad del usuario. 
    
    # Configurar figura para visualización
    plt.figure(figsize=(12, 12))  # Tamaño grande para mejor visualización
    
    # Dibujar elementos del grafo:
    # 1. Nodos con color de comunidad (fondo)
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color=color_comunidad, alpha=0.6)
    # 2. Aristas con transparencia
    nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.5)
    # 3. Nodos con color de estado (sobreposición)
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color=color_nodos, alpha=0.6)
    # 4. Etiquetas numéricas de nodos
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")
    
    # Añadir título con paso de tiempo actual
    plt.title(f"{titulo} - Tiempo {i}")
    # Mostrar gráfico
    plt.show()


#----------------------------------------------------------------------------------------------------
# Función que actualiza el grafo con una nueva red SBM en cada tiempo i
def actualizar_red(G, kave, numero_de_individuos, bloques, P, comunidades, var_de_prob):
    # Obtener los tamaños de las comunidades
    tamanos = [len(comunidad) for comunidad in comunidades]
    
    # Variar las probabilidades de conexión entre comunidades en cada paso temporal
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            # Ajuste aleatorio de la probabilidad de conexión entre comunidades
            P[i][j] += random.uniform(-var_de_prob, var_de_prob)  # Pequeña variación en las probabilidades entre comunidades
            P[j][i] = P[i][j]  # La matriz es simétrica
            
            # Asegurarse de que los valores estén entre 0 y 1
            P[i][j] = max(0, min(1, P[i][j]))
            P[j][i] = P[i][j]
    
    # Re-generar la red con la nueva matriz de probabilidades
    G_nueva = nx.stochastic_block_model(tamanos, P)
    return G_nueva, P


#----------------------------------------------------------------------------------------------------
# Función para mostrar el heatmap de conexiones entre comunidades de manera dinámica
def mostrar_heatmap_conexiones(P, i):
    # Mostrar el heatmap de las probabilidades de conexión entre las comunidades
    plt.figure(figsize=(8, 6)) #Tamaño de la figura la cual se puede modificar segun el usuario lo requiera.
    cax = plt.imshow(P, cmap='YlGnBu', interpolation='nearest')
    plt.colorbar(cax)
    plt.title(f"Heatmap de conexiones entre comunidades - Tiempo {i}")
    plt.xlabel("Comunidades")
    plt.ylabel("Comunidades")
    
    # Etiquetas con la probabilidad de conexión en cada bloque
    for i in range(len(P)):
        for j in range(len(P)):
            plt.text(j, i, f'{P[i][j]:.2f}', ha='center', va='center', color='black', fontsize=8)
    
    plt.xticks(ticks=np.arange(len(P)), labels=[f'Comuni {i}' for i in range(len(P))], rotation = 90) # Como la palabra comunidad no cabe en mi heatmap de manera adecuada entonces lo simplifico como "comuni"
    plt.yticks(ticks=np.arange(len(P)), labels=[f'Comunidad {i}' for i in range(len(P))])
    plt.show()

#---------------------------------------------------------------------------------------------------
#Funcion principal la cual dependera de otras funciones para poder realizar la simulación dinamica SBM
#Tener mucho cuidado al modificar esta parte ya que es primordial en el codigo y cualquier cambio puede afectar el funcionamiento. 
def simular_sbm_dinamico(t, N, tau, gamma, kave, rho, numero_de_individuos, bloques,probabilidad_externa_base,var_de_prob):
    # Colores llamativos para las comunidades
    colores_comunidades = ['#FF6347', '#FFD700', '#FF1493', '#00FFFF', '#32CD32', '#8A2BE2', '#FF4500', '#9ACD32', '#DA70D6', '#FF8C00']

    for z in range(1,N+1):
        #Las siguientes funciones ayudaran a tener un estandar para la simulacion la cual se trabajara hasta el N dado y en el tiempo i dado.
        G, comunidades, P = generar_red_SBM(kave, numero_de_individuos, bloques, probabilidad_externa_base)
        sim = aplicar_gillespie(G, tau, gamma, rho, t)

        for i in range(1, t+1):
            print(f"\n--- Tiempo {i} ---")

            infectados, recuperados = mostrar_estados(G, sim, i) #Invocando la funcion podemos ver los estados de los individuos ojo esta linea es muy importante.
            
            serie_temporal(sim, i) #Invocamos la funcion para ver la serie temporal, esta funcion puede ocuparse o no ya que solo muestra el estado de la simulacion graficamente, por lo tanto no existe problema si se elimina esta linea.
            
            visualizar_red_sbm(G, sim, i, comunidades, colores_comunidades, titulo=f"Red SBM en tiempo {i}")  # Visualización de la red en cada paso
            
            mostrar_heatmap_conexiones(P, i)  # Mostrar el heatmap de conexiones entre comunidades

            G, P = actualizar_red(G, kave, numero_de_individuos, bloques, P, comunidades,var_de_prob)  # Actualizar la red en cada tiempo i para ver el comportamiento dinamico de la red.

#----------------------------------------------------------------------------------------------------
# Parámetros de simulación.
t = 10  # Duración de la simulación el valor de t tiene que se un entero positivo t > 0
N = 1  # Número de redes simuladas el valor de N tiene que ser un entero positivo N > 0
gamma = 0.01  # Tasa de recuperación gamma tiene que estar entre 0 < gamma < 1 ya que esto marcara el como se recupera cada individuo osea su probabilidad de salir de una enfermedad.
rho = 0.2  # Fracción inicial de infectados la variable rho tiene que estar acotada entre 0 < tau < 1 donde 0 es es una polacion sin infectados y 1 la poblacion totalmente infectada. 
kave = 5  # Grado promedio de conexiones en la red
tau = 2 * gamma / kave  # Tasa de transmisión (Esta formula es parecida a la tasa de transmision de datos o información).
numero_de_individuos = 300  # Número de nodos o de individuos a simular este valor tiene que estar en el conjunto de los enteros positivos  numero_de_individuos > 1
bloques = 8  # Número de comunidades, esta variable tiene que estar en los enteros positivos, bloques > 0 por que no se pueden tener comunidades a medias o bueno no seria lo ideal 
probabilidad_externa_base = 0.01 # Probabilidad base de conexión entre comunidades (puede variar entre pasos) al ser una probabilidad recordar que cualquier probabilidad debe de estar entre 0 y 1.
var_de_prob=1 # Esta variable generara una variacion de las probabilidades entre las comunidades dependiendo el valor que se de, su dominio sera acotado por ese mismo valor en la parte negativa y positiva. Igualmente acostada entre 0 y 1.
# la misma var_de_prob dara el maximo valor de probabilidad que quiera el usuario. 


simular_sbm_dinamico(t, N, tau, gamma, kave, rho, numero_de_individuos, bloques,probabilidad_externa_base, var_de_prob) # Ojo esta parte ayuda a invocar la funcion primordial,
#En caso de no tomar en cuenta esta informacion, el usuario es responsable del mal funcionamiento del sistema dinamico. 
