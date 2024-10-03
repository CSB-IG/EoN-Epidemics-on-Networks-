import networkx as nx
import EoN
import matplotlib.pyplot as plt

N=10000#Numero de población 
gamma = 1 # tasa de recuperación 
rho = 0.05 # Suponemos una red con un grado promedio de 20. La condición inicial
#es que una fracción ρ (rho) de la población se infecta al azar.
kave = 20#grado de nodos. 
tau = 2*gamma/ kave # tasa de transmisión 
S0 = (1-rho)*N #Número inicial susceptible 
I0 = rho*N # Número inicial de infectados 
SI0 = (1-rho)*kave*rho*N # número inicial de aristas del SI 
SS0 = (1-rho)*kave*(1-rho)*N # Número inicial de aristas SS 
t, S, I = EoN.SIS_homogeneous_pairwise(S0, I0, SI0, SS0, kave, tau, gamma,
tmax=10) # esto se suele denominar “modelo de campo medio cerrado a nivel de triples”.

plt.plot(t, S, label = "S")
plt.plot(t, I, label = "I")
plt.xlabel("$t$")
plt.ylabel("Números previstos")
plt.legend()
plt.show()
