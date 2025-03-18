import networkx as nx
import EoN
import random
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
#---------------------------------------------------------------------------------------------------
def generar_red_SBM(kave, numero_de_individuos, bloques):
  tam = [numero_de_individuos // bloques] * bloques
  
  
#---------------------------------------------------------------------------------------------------
#Funcion principal la cual dependera de otras funciones para poder realizar la simulación dinamica SBM
def simular_sbm_dinamico(t, N, tau, gamma, kave, rho, numero_de_individuos, bloques):
  # Colores llamativos para las comunidades
  colores_comunidades = ['#FF6347', '#FFD700', '#FF1493', '#00FFFF', '#32CD32', '#8A2BE2', '#FF4500', '#9ACD32', '#DA70D6', '#FF8C00']
    


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

simular_sbm_dinamico(t, N, tau, gamma, kave, rho, numero_de_individuos, bloques)
