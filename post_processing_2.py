import matplotlib.pyplot as plt
import numpy as np

bn = []
while True:
    try:
        x = float(input())
        bn.append(x)
    except:
        break

valores_betweenness_aristas = bn

plt.hist(valores_betweenness_aristas, bins=20, color='purple')
plt.xlabel('Betweenness de aristas')
plt.ylabel('Frecuencia')
plt.title('Distribución del betweenness de las aristas')
plt.savefig('distribucion_betweenness_aristas.png')
plt.clf()
