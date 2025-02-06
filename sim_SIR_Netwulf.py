import networkx as nx
import EoN
import netwulf as nw


# Función que genera la red
def generar_red(kave, numero_de_individuos):
    infec_ratio = kave / (numero_de_individuos - 1)
    G_i = nx.fast_gnp_random_graph(numero_de_individuos, infec_ratio)
    return G_i

#-----------------------------------------------------------------------------------------------------------------
# Función que aplica la simulación Gillespie SIR
def aplicar_gillespie(G, tau, gamma, rho, t):
    sim = EoN.Gillespie_SIR(G, tau, gamma, rho=rho, tmax=t, return_full_data=True)
    return sim

#-----------------------------------------------------------------------------------------------------------------
# Función que conserva los nodos conectados y muestra el resultado final en el tiempo t
def conservar_nodos_conectados(G, sim, t):
    # Inicializar un conjunto para almacenar todos los nodos conectados
    nodos_conectados = set()

    # Recorrer todos los tiempos desde t=1 hasta t
    for tiempo in range(1, t + 1):
        estados = sim.get_statuses(time=tiempo)
        # Agregar nodos que estuvieron conectados en este tiempo
        for u, v in G.edges():
            if estados[u] != 'S' or estados[v] != 'S':  # Si alguno de los nodos no es susceptible
                nodos_conectados.add(u)
                nodos_conectados.add(v)

    # Obtener los estados finales en el tiempo t
    estados_finales = sim.get_statuses(time=t)
    
    # Crear un grafo para visualizar la red final
    arbol_transmision = nx.DiGraph()

    # Agregar solo los nodos que estuvieron conectados en algún momento
    for nodo in nodos_conectados:
        arbol_transmision.add_node(nodo)
        if estados_finales[nodo] == 'I':
            arbol_transmision.nodes[nodo]['color'] = 'red'  # Infectados en rojo
        elif estados_finales[nodo] == 'R':
            arbol_transmision.nodes[nodo]['color'] = 'Aqua'  # Recuperados en Aqua
        else:
            arbol_transmision.nodes[nodo]['color'] = 'green'  # Susceptibles en verde

    # Agregar las aristas que conectan los nodos en el tiempo final
    for u, v in G.edges():
        if u in nodos_conectados and v in nodos_conectados:
            arbol_transmision.add_edge(u, v, label=f"t={t}")

    return arbol_transmision

#--------------------------------------------------------------------------------------------------------------
# Función principal que organiza la simulación y las visualizaciones
def generar_redes_transmision(t, tau, gamma, N, kave, rho, numero_de_individuos):
    for z in range(1, N + 1):
        G = generar_red(kave, numero_de_individuos)  # Generar la red
        sim = aplicar_gillespie(G, tau, gamma, rho, t)  # Aplicar la simulación SIR

        # Conservar los nodos conectados y obtener el grafo final
        arbol_transmision = conservar_nodos_conectados(G, sim, t)

        # Visualizar con netwulf en el último tiempo t
        print(f"\n--- Visualización de la red en el último tiempo t={t} ---")

        # Especificar un puerto diferente para netwulf
        nw.visualize(arbol_transmision)  


#--------------------------------------------------------------------------------------------------------------

# Parámetros de simulación
t = 20  # Duración de la simulación
N = 1  # Número de redes a simular
gamma = 0.2  # Tasa de recuperación
rho = 0.1  # Fracción inicial de nodos infectados
kave = 5  # Grado promedio de conexiones en la red
tau = 2 * gamma / kave  # Tasa de transmisión
numero_de_individuos = 500  # Número de individuos en la población (reducido para pruebas)

# Llamado de la función principal
generar_redes_transmision(t, tau, gamma, N, kave, rho, numero_de_individuos)

#--------------------------------------------------------------------------------------------------------------

'''Como se puede observar, el código es muy parecido al código Simulacion_Red_SIR_correcta.py.
Lo que se quiso observar fue si era posible adaptar el sistema dinámico antes mencionado con la librería Netwulf, 
ya que esta misma tiene una visualización muy interactiva y pensé que podría ser de gran utilidad. 
Sin embargo, resultó que solo muestra los resultados en una sola ocasión y no es posible ver cada tiempo tt.
 Por eso, adapté el código para solo ver el tiempo t=final. Quien logre poner antecion en los comentarios de este codigo recuerden que 
este codigo me llevo horas extra de servicio social en el INMEGEN y bastante tiempo de analisis. (Echo por Jesús Mauricio Flores de Modelación Matemática SLT UACM)

M4uroCube.'''
