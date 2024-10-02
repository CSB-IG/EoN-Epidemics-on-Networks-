import networkx as nx
import EoN
import matplotlib.pyplot as plt

N = 10**5 #Numero de individuos 
kave = 5 #Numero esperado de compañeros
print("generando gráfico G con {} nodos".format(N))

G = nx.fast_gnp_random_graph(N, kave/(N-1)) #Erdo’’s-Re’nyi  gráfico aleatorio, gráfico binomial.
rho = 0.005 #fraccion inicial de infectados 
tau = 0.3 #rango de transmision
gamma = 1.0 #Tasa de recuperacion
print("Realizar simulación basada en eventos")
t1, S1, I1 = EoN.fast_SIS(G, tau, gamma, rho=rho, tmax = 30)
#Simulaciones rápidas de SIS para epidemias en redes ponderadas o no ponderadas, 
#que permiten que los pesos de los nodos y los bordes escalen las tasas de transmisión 
#y recuperación. Supone tiempos de recuperación y transmisión distribuidos exponencialmente.
print("haciendo simulación de Gillespie")
t2, S2, I2 = EoN.Gillespie_SIS(G, tau, gamma, rho=rho, tmax = 30)#Simulaciones rapidas de SIS con Gillespei
print("Terminé con las simulaciones, ahora estoy trazando")

plt.plot(t1, I1, label = "rapido_SIS")
plt.plot(t2, I2, label = "Gillespie_SIS")
plt.xlabel("$t$")
plt.ylabel("Number infected")
plt.legend()
plt.show()
