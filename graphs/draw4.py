import networkx as nx
import matplotlib.pyplot as plt
import random

def draw_colored_graph_from_file(filename):
    # Leer las aristas desde el archivo
    edges = []
    with open(filename, 'r') as file:
        for line in file:
            u, v = map(int, line.split())  # Convierte los nodos a enteros
            edges.append((u, v))
    
    # Crear el grafo
    G = nx.Graph()
    G.add_edges_from(edges)
    
    # Generar colores aleatorios para cada nodo
    nodes = G.nodes()
    colors = [random.random() for _ in nodes]
    
    # Dibujar el grafo
    pos = nx.spring_layout(G)  # Disposición de los nodos
    nx.draw(
        G, 
        pos, 
        node_color=colors, 
        cmap=plt.cm.rainbow, 
        with_labels=False, 
        node_size=500
    )
    plt.show()

# Ejemplo de uso
filename = input()  # Nombre del archivo con las aristas
draw_colored_graph_from_file(filename)
import networkx as nx
import matplotlib.pyplot as plt
import random

def draw_colored_graph_from_file(filename):
    # Leer las aristas desde el archivo
    edges = []
    with open(filename, 'r') as file:
        for line in file:
            u, v = map(int, line.split())  # Convierte los nodos a enteros
            edges.append((u, v))
    
    # Crear el grafo
    G = nx.Graph()
    G.add_edges_from(edges)
    
    # Generar colores aleatorios para cada nodo
    nodes = G.nodes()
    colors = [random.random() for _ in nodes]
    
    # Dibujar el grafo
    pos = nx.spring_layout(G, k=500, iterations=100)  # Aumenta 'k' para separar nodos
    nx.draw(
        G, 
        pos, 
        node_color=colors, 
        cmap=plt.cm.rainbow, 
        with_labels=False, 
        node_size=500
    )
    plt.show()

# Ejemplo de uso
filename = 'minors.out'  # Nombre del archivo con las aristas
draw_colored_graph_from_file(filename)
