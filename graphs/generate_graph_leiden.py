import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import Counter
import igraph as ig
import leidenalg as la

# Paso 1: Cargar los datos
problems_df = pd.read_csv('codeforces_problems.csv')
similarity_df = pd.read_csv('similarity_dict.csv')

# Paso 2: Filtrar el archivo similarity_dict por el umbral de similitud
similarity_threshold = 0.8
filtered_similarity = similarity_df[similarity_df['similarity'] > similarity_threshold]

# Paso 3: Crear el grafo con NetworkX
G_nx = nx.Graph()

# Añadir nodos desde el archivo de problemas
for _, row in problems_df.iterrows():
    problem_id = row['Problem ID']
    tags = row['Tags']
    description = row['Description']
    rating = row['Rating']
    url = row['Problem URL']
    G_nx.add_node(problem_id, tags=tags, description=description, rating=rating, url=url)

# Añadir aristas según el archivo de similaridades filtrado
for _, row in filtered_similarity.iterrows():
    id1 = row['id1']
    id2 = row['id2']
    similarity = row['similarity']
    G_nx.add_edge(id1, id2, weight=similarity)

# Paso 4: Convertir el grafo NetworkX a un grafo igraph
G_ig = ig.Graph.TupleList(G_nx.edges(data=True), edge_attrs=['weight'])

# Paso 5: Aplicar el algoritmo de Leiden
partition = la.find_partition(G_ig, la.CPMVertexPartition, resolution_parameter=0.1)

# Crear un diccionario de comunidades para NetworkX
partition_dict = {G_ig.vs[i]["name"]: community for i, community in enumerate(partition.membership)}

# Contar el tamaño de cada comunidad
community_counts = Counter(partition_dict.values())

# Añadir las comunidades como atributo en el grafo NetworkX
for node, community in partition_dict.items():
    G_nx.nodes[node]['community'] = community

# Guardar el grafo con comunidades en formato GraphML
nx.write_graphml(G_nx, "codeforces_community_graph_2.graphml")
print("Grafo guardado como 'codeforces_community_graph_2.graphml'")

# Filtrar los nodos de comunidades con más de 10 miembros
#filtered_nodes = [node for node, community in partition_dict.items() if community_counts[community] > 10]

# Crear un subgrafo con solo estos nodos
G_filtered = G_nx#.subgraph(filtered_nodes)

# Elegir una submuestra si el grafo filtrado aún es grande
sample_size = 2000  # Ajusta según el tamaño del grafo
if G_filtered.number_of_nodes() > sample_size:
    sampled_nodes = random.sample(list(G_filtered.nodes), sample_size)
    G_subgraph = G_filtered.subgraph(sampled_nodes)
else:
    G_subgraph = G_filtered

# Asignar colores a las comunidades
unique_communities = set(partition_dict.values())
community_colors = {com: plt.cm.tab20(i % 20) for i, com in enumerate(unique_communities)}
node_colors = [community_colors[G_subgraph.nodes[node]['community']] for node in G_subgraph.nodes]

# Dibujar y guardar el grafo
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G_subgraph, seed=42)
nx.draw_networkx_nodes(G_subgraph, pos, node_size=50, node_color=node_colors)
nx.draw_networkx_edges(G_subgraph, pos, alpha=0.3, edge_color="gray")
plt.axis("off")
plt.title("Grafo de Problemas Codeforces con Comunidades Detectadas (Leiden)")
plt.savefig("codeforces_communities_graph_leiden.png", format="PNG", dpi=300)
plt.show()
