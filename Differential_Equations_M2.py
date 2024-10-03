import networkx as nx
import EoN
import matplotlib.pyplot as plt
import numpy as np

gamma = 1# tasa de recuperación por nodo 
tau = 1.5# tasa de transmisión de borde 
kave = 3 # #grado de nodos. 
rho = 0.01# Suponemos una red con un grado promedio de 20. La condición inicial
#es que una fracción ρ (rho) de la población se infecta al azar.
phiS0 = 1-rho# proporción inicial de bordes (de nodos susceptibles) que se conectan a nodos susceptibles 

def psi(x):
	return (1-rho)* np.exp(-kave*(1-x))

def psiPrime(x):
	return (1-rho)*kave*np.exp(-kave*(1-x))# donde S(k,0) es la probabilidad de que un nodo 
	#aleatorio tenga grado k y sea susceptible en el momento de inicio. 
#Cualquirer duda con las funciones utilizadas ver la pagina 9 del articulo 
# EoN (Epidemics on Networks): a fast, flexible Python
#package for simulation, analytic approximation, and
#analysis of epidemics on networks.

N=1# tamaño de la población .

t, S, I, R = EoN.EBCM(N, psi, psiPrime, tau, gamma, phiS0, tmax = 10)# Modelo EBCM

plt.plot(t, S, label = "S")
plt.plot(t, I, label = "I")
plt.plot(t, R, label = "R")
plt.xlabel("$t$")
plt.ylabel("Proporciones previstas")
plt.legend()
plt.show()
