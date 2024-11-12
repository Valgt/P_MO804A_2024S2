import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Cargar el grafo desde el archivo .graphml
grafo = nx.read_graphml('codeforces_community_graph.graphml')

bn = []
while True:
    try:
        x = int(input())
        bn.append(x)
    except:
        break

num_componentes_list = bn

plt.plot(range(1, len(num_componentes_list) + 1), num_componentes_list, marker='o', color='red')
plt.xlabel('Número de nodos eliminados')
plt.ylabel('Número de componentes conectados')
plt.title('Cambio en el número de componentes al eliminar nodos con mayor betweenness')
plt.savefig('cambio_componentes.png')
plt.clf()

# Distribución de grados y grado medio
grados_nodos = [grado for nodo, grado in grafo.degree()]
grado_medio = np.mean(grados_nodos)
plt.hist(grados_nodos, bins=20, color='orange')
plt.xlabel('Grado de los nodos')
plt.ylabel('Frecuencia')
plt.title('Distribución del grado de los nodos')
plt.savefig('distribucion_grados.png')
plt.clf()
print(f"Grado medio del grafo: {grado_medio}")

# Visualización del grafo (guardar como imagen)
plt.figure(figsize=(10, 10))
nx.draw(grafo, node_size=20, node_color='skyblue', edge_color='gray', with_labels=False)
plt.title('Visualización del grafo')
plt.savefig('visualizacion_grafo.png')
plt.clf()
