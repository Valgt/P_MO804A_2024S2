import networkx as nx
import matplotlib.pyplot as plt

# Cargar el grafo en formato GraphML
def load_graph(graphml_file):
    return nx.read_graphml(graphml_file)

# Comprimir las comunidades y crear el nuevo grafo
def compress_communities(G, min_size=20):
    new_graph = nx.Graph()

    # Filtrar las comunidades por tamaño
    community_sizes = {}
    for node in G.nodes:
        community_id = G.nodes[node].get('community')
        if community_id not in community_sizes:
            community_sizes[community_id] = 0
        community_sizes[community_id] += 1
    
    # Agregar solo las comunidades con al menos 'min_size' nodos
    for node in G.nodes:
        community_id = G.nodes[node].get('community')
        if community_sizes[community_id] >= min_size:
            if community_id not in new_graph:
                new_graph.add_node(community_id)

    # Agregar aristas entre las comunidades con el peso correspondiente
    for u, v in G.edges:
        community_u = G.nodes[u].get('community')
        community_v = G.nodes[v].get('community')
        if community_u != community_v:
            # Solo agregar aristas si ambas comunidades tienen al menos 'min_size' nodos
            if community_sizes[community_u] >= min_size and community_sizes[community_v] >= min_size:
                if new_graph.has_edge(community_u, community_v):
                    new_graph[community_u][community_v]['weight'] += 1
                else:
                    new_graph.add_edge(community_u, community_v, weight=1)
    
    return new_graph

# Guardar el grafo comprimido en formato GraphML
def save_compressed_graph(new_graph, output_file):
    nx.write_graphml(new_graph, output_file)

# Visualizar el grafo comprimido
def visualize_graph(new_graph):
    # Usar un layout alternativo si el actual no está funcionando bien
    pos = nx.spring_layout(new_graph, k=0.15, iterations=20)  # Ajusta 'k' y las iteraciones si es necesario

    plt.figure(figsize=(12, 10))

    # Obtener los pesos de las aristas
    edge_weights = [new_graph[u][v]['weight'] for u, v in new_graph.edges]

    # Normalizar los pesos de las aristas para ajustar el grosor
    min_weight = min(edge_weights)
    max_weight = max(edge_weights)
    edge_widths = [2 + 8 * (weight - min_weight) / (max_weight - min_weight) for weight in edge_weights]

    # Dibujar el grafo con el grosor de las aristas ajustado al peso
    nx.draw(new_graph, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray', width=edge_widths)

    # Dibujar las etiquetas de los pesos de las aristas
    labels = nx.get_edge_attributes(new_graph, 'weight')
    nx.draw_networkx_edge_labels(new_graph, pos, edge_labels=labels, font_size=8, font_weight='bold')

    plt.axis('off')  # Eliminar el eje para una visualización más limpia
    plt.show()

def main():
    graphml_file = 'codeforces_community_graph.graphml'

    # Cargar el grafo original
    G = load_graph(graphml_file)

    # Comprimir las comunidades en un nuevo grafo, eliminando comunidades con menos de 20 nodos
    new_graph = compress_communities(G, min_size=20)

    # Guardar el nuevo grafo comprimido
    output_file = 'codeforces_community_graph_redux.graphml'
    save_compressed_graph(new_graph, output_file)

    # Visualizar el grafo comprimido
    visualize_graph(new_graph)

if __name__ == "__main__":
    main()
