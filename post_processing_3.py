import matplotlib.pyplot as plt
import numpy as np

dl = []
t = 0
while True:
    try:
        x = int(input())
        x = int(np.log(x + 1))
        while x > 0:
            dl.append(t)
            x -= 1
        t += 1
    except:
        break

distancias_lista = dl

plt.hist(distancias_lista, bins=20, color='salmon')
plt.xlabel('Distancia entre nodos')
plt.ylabel('Frecuencia')
plt.title('Distribución de distancias entre nodos (ln)')
plt.savefig('distribucion_distancias.png')
plt.clf()
