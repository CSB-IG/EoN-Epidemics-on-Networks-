import networkx as nx
import EoN
import matplotlib.pyplot as plt
from collections import defaultdict
import random

#----------------------------------------------------------------------------------------------------------------------
# Función que genera una red en cuadrícula 2D con vacunación
def generar_red_cuadrada_con_vacunacion(dimensiones, prob_vacunacion):
    
    G = nx.grid_2d_graph(*dimensiones)  # Crear una red cuadrada 2D
    initial_infections = [(u, v) for (u, v) in G if 45 < u < 55 and 45 < v < 55]
    vacunados = [nodo for nodo in G if random.random() < prob_vacunacion]
    
    # Definir estado inicial: susceptibles, infectados o vacunados
    IC = defaultdict(lambda: "Sus")
    for nodo in initial_infections:
        IC[nodo] = "Inf"
    for nodo in vacunados:
        IC[nodo] = "Vac"
    
    return G, IC

#--------------------------------------------------------------------------------------------------------------------
# Función que aplica la simulación de Gillespie con vacunación y recuperación
def aplicar_gillespie_con_vacunacion(G, IC, tmax,SVr,IRr,Tir):
    
    H = nx.DiGraph()  # Transiciones espontáneas
    H.add_edge("Sus", "Vac", rate=SVr)
    H.add_edge("Inf", "Rec", rate=IRr)
    
    J = nx.DiGraph()  # Transiciones inducidas
    J.add_edge(("Inf", "Sus"), ("Inf", "Inf"), rate=Tir)

    color_dict = {'Sus': '#009a80','Inf':'#ff2000', 'Rec':'gray','Vac': '#5AB3E6'}
    pos = {node:node for node in G}
    tex = False
    sim_kwargs = {'color_dict':color_dict, 'pos':pos, 'tex':tex}

    return_statuses = ["Sus", "Inf", "Rec", "Vac"]
    sim = EoN.Gillespie_simple_contagion(G, H, J, IC, return_statuses, tmax=tmax, return_full_data=True,sim_kwargs=sim_kwargs)
    
    return sim

#---------------------------------------------------------------------------)---------------------------------------
# Función para graficar la serie temporal de la simulación
def graficar_serie_temporal(sim):
        
        times, D = sim.summary()
        newD = {"Sus+Vac": D["Sus"] + D["Vac"], "Inf+Rec": D["Inf"] + D["Rec"]}
        new_timeseries = (times, newD)
        sim.add_timeseries(new_timeseries, label="Simulation", color_dict={"Sus+Vac": "#E69A00", "Inf+Rec": "#CD9AB3"})

        plt.figure(figsize=(10, 6))
        plt.plot(times, D["Sus"], label="Susceptibles", color="#009a80")
        plt.plot(times, D["Inf"], label="Infectados", color="#ff2000")
        plt.plot(times, D["Rec"], label="Recuperados", color="gray")
        plt.plot(times, D["Vac"], label="Vacunados", color="#5AB3E6")
        plt.xlabel("Tiempo")
        plt.ylabel("Número de individuos")
        plt.title("Serie Temporal de Susceptibles, Infectados, Recuperados y Vacunados")
        plt.legend()
        plt.grid()
        plt.show()

#-------------------------------------------------------------------------------------------------------------------

# Función para mostrar la red en tiempo real
def mostrar_simulacion_en_red(sim, G, tmax):

    color_dict = {"Sus": "#009a80", "Inf": "#ff2000", "Rec": "gray", "Vac": "#5AB3E6"}
    pos = {node: node for node in G}  # La posición es la misma en la cuadrícula

    # Obtener el estado de los nodos en el momento final
    nodestatus = sim.get_statuses(time=tmax)
    node_colors = [color_dict[nodestatus[node]] for node in G.nodes()]

    plt.figure(figsize=(10, 10))
    nx.draw(G, pos=pos, node_color=node_colors, node_size=4)
    plt.title(f"Estado de la red en el tiempo t={tmax}")
    plt.show()

#---------------------------------------------------------------------------------------------------------------

# Función para generar la animación de la simulación
def generar_animacion(sim):
    
    # Generar animación con los parámetros deseados
    ani = sim.animate(ts_plots=[["Inf"], ["Sus+Vac", "Inf+Rec"]], node_size=4)
    ani.save("SIRV_animate2.mp4", fps=5, extra_args=["-vcodec", "libx264"])

#---------------------------------------------------------------------------------------------------------------

# Función principal para ejecutar la simulación completa
def ejecutar_simulacion_vacunacion(dimensiones,prob_vacunacion,t,SVr,IRr,Tir):
    
    #Funcion para generar la red con vacunados.
    G, IC = generar_red_cuadrada_con_vacunacion(dimensiones, prob_vacunacion)
    
    #Se muestra la grafica en cada tiempo t
    for i in range(t):
        #Simulacion de gillespie con vacunados
        sim = aplicar_gillespie_con_vacunacion(G, IC, i, SVr, IRr, Tir,)
    
        #Serie temporal para observar el comportamiento
        graficar_serie_temporal(sim)
#------------------------------------------------------------------------------------
    #Mostramos la simulacion de la red.
    mostrar_simulacion_en_red(sim, G, t)
    
    #---------------------------------------------------------------------------------------
    # Llamada a la función de animación para tener un video en tiempo real.
    # generar_animacion(sim)  

#-------------------------------------------------------------------------------------------------------------------------------------
#Parametros que se pueden ambiar segun sea el caso necesario para simular el comportamiento de una pandemia.
#Dimesión de la población 
dimensiones=(100,100)
#Vacunación en la población 
prob_vacunacion=0.2 #0.3
#Tiempo de simulación
t=20
#--------------------------------------------------------------------------------------------------------------------------------------
#Transiciones espontáneas
SVr=0.01#Susceptible-vacunado 0.01
IRr=0.1 #Infectado-Recuperado 0.1
#---------------------------------------------------------------------------------------------------------------------------
# Transiciones inducidas
Tir=1.5 #2.0
#---------------------------------------------------------------------------------------------------------------------------
# Llamada a la función principal
ejecutar_simulacion_vacunacion(dimensiones, prob_vacunacion, t, SVr, IRr, Tir)

#---------------------------------------------------------------------------------------------------------------------------

#Con este modelo se puede observar como se comporta la enfermedad, aunque un video es mucho mejor para ver como se comporta el modelo.
#(Echo por Jesús Mauricio Flores de Modelación Matemática SLT UACM)

#M4uroCube.
