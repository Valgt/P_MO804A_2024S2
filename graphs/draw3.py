import networkx as nx
import random
import matplotlib.pyplot as plt

# Cargar el grafo en formato GraphML
def load_graph(graphml_file):
    return nx.read_graphml(graphml_file)

# Comprimir aleatoriamente un porcentaje de aristas
def compress_random_edges(G, percentage=99.9995):
    # Número total de aristas en el grafo
    total_edges = list(G.edges)
    
    # Calcular el número de aristas a seleccionar según el porcentaje
    num_edges_to_compress = int(len(total_edges) * (percentage / 100))
    
    # Seleccionar aleatoriamente las aristas a comprimir
    edges_to_compress = random.sample(total_edges, num_edges_to_compress)

    # Crear un nuevo grafo para almacenar el grafo comprimido
    new_graph = nx.Graph()

    # Agregar nodos del grafo original al nuevo grafo
    new_graph.add_nodes_from(G.nodes)

    # Comprimir las aristas seleccionadas
    for u, v in edges_to_compress:
        # Comprimir la arista entre u y v como una nueva arista en el grafo comprimido
        if not new_graph.has_edge(u, v):
            new_graph.add_edge(u, v, weight=1)
        else:
            new_graph[u][v]['weight'] += 1

    return new_graph

# Guardar el grafo comprimido en formato GraphML
def save_compressed_graph(new_graph, output_file):
    nx.write_graphml(new_graph, output_file)

# Visualizar el grafo comprimido
def visualize_graph(new_graph):
    pos = nx.spring_layout(new_graph, k=0.15, iterations=20)
    plt.figure(figsize=(12, 10))

    # Obtener los pesos de las aristas
    edge_weights = [new_graph[u][v]['weight'] for u, v in new_graph.edges]
    min_weight = min(edge_weights)
    max_weight = max(edge_weights)
    
    # Si todos los pesos son iguales, asignamos un grosor constante
    if max_weight == min_weight:
        edge_widths = [2 for _ in edge_weights]
    else:
        # Ajustar grosor de las aristas según su peso
        edge_widths = [2 + 8 * (weight - min_weight) / (max_weight - min_weight) for weight in edge_weights]

    # Dibujar el grafo
    nx.draw(new_graph, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray', width=edge_widths)
    
    # Dibujar las etiquetas de los pesos de las aristas
    labels = nx.get_edge_attributes(new_graph, 'weight')
    nx.draw_networkx_edge_labels(new_graph, pos, edge_labels=labels, font_size=8, font_weight='bold')

    plt.axis('off')
    plt.show()

def main():
    graphml_file = 'codeforces_community_graph.graphml'

    # Cargar el grafo original
    G = load_graph(graphml_file)

    # Comprimir aleatoriamente un porcentaje de aristas (por ejemplo, 70%)
    new_graph = compress_random_edges(G)

    # Guardar el nuevo grafo comprimido
    output_file = 'codeforces_community_graph_compressed.graphml'
    save_compressed_graph(new_graph, output_file)

    # Visualizar el grafo comprimido
    visualize_graph(new_graph)

if __name__ == "__main__":
    main()
