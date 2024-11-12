import matplotlib.pyplot as plt
import numpy as np

input()
bn = []
while True:
    try:
        x = float(input())
        if abs(x - 1) < 1e-6:
            continue
        bn.append(x)
    except:
        break

valores_betweenness_nodos = bn

plt.hist(valores_betweenness_nodos, bins=100, range=(0, 0.06), color='lightgreen')
plt.xlabel('Betweenness de nodos')
plt.ylabel('Frecuencia')
plt.title('Distribución del betweenness de los nodos')
plt.savefig('distribucion_betweenness_nodos.png')
plt.clf()