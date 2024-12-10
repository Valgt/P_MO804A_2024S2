import networkx as nx
from collections import Counter

# Función para obtener los tags en una comunidad específica, ordenados por frecuencia
def get_tags_in_community(graph, community_id):
    tags_counter = Counter()

    # Iterar sobre todos los nodos en el grafo
    for node, data in graph.nodes(data=True):
        # Verificar si el nodo pertenece a la comunidad deseada
        if data.get("community", "") == community_id:
            # Obtener los tags del nodo desde la clave específica 'd0'
            tags_str = data.get("tags", "")
            tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
            
            # Actualizar el contador con los tags
            tags_counter.update(tags)

    # Ordenar los tags por frecuencia de mayor a menor
    sorted_tags = tags_counter.most_common()
    return sorted_tags

# Cargar el grafo
G_nx = nx.read_graphml("codeforces_community_graph_2.graphml")

# Ejemplo de uso: Obtener los tags en una comunidad específica
community_id = int(input("Ingresa el ID de la comunidad: "))
tags_in_community = get_tags_in_community(G_nx, community_id)

# Mostrar los tags ordenados de mayor a menor frecuencia
if tags_in_community:
    print(f"Tags en la comunidad '{community_id}' ordenados por frecuencia:")
    for tag, count in tags_in_community:
        print(f"{tag}: {count}")
else:
    print(f"No se encontraron tags en la comunidad '{community_id}'.")
