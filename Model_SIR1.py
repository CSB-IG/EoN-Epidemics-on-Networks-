import networkx as nx
import EoN
import matplotlib.pyplot as plt

N = 10**6 #numeros individuales
kave = 5 #Numero esperado de infectados

print("generando gráfico G con {} nodos".format(N))

G = nx.fast_gnp_random_graph(N, kave/(N-1)) #Gráfico Erdo's-Re'nyi generado con N numero de individuos y el 
#numero esperado de individuos
rho = 0.005 #fracción inicial infectada
tau = 0.3 #rango de transmision
gamma = 1.0 #tasa de recuperación

print("haciendo simulación basada en eventos")
t1, S1, I1, R1 = EoN.fast_SIR(G, tau, gamma, rho=rho)#EoN.fast_SIR genera una Simulación SIR rápida para tiempos de infección y recuperación distribuidos exponencialmente
#en lugar de rho, podríamos especificar una lista de nodos como inicial_infectados, o
#no especifique ninguno y se elegirá un único nodo aleatorio como caso índice.

print("haciendo simulación de Gillespie")

t2, S2, I2, R2 = EoN.Gillespie_SIR(G, tau, gamma, rho=rho)# Realiza simulaciones SIR para epidemias.

print("Trazando")
plt.plot(t1, I1, label = "rápido_SIR")
plt.plot(t2, I2, label = "Gillespie_SIR")
plt.xlabel("$t$")
plt.ylabel("Numero de infectados")
plt.legend()
plt.show()
