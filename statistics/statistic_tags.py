import networkx as nx
import pandas as pd
import re

# Cargar el grafo
G = nx.read_graphml("codeforces_community_graph_2.graphml")

# Crear DataFrame con nodos y atributos para un análisis más sencillo
node_data = []
for node, data in G.nodes(data=True):
    data['problem_id'] = node  # Agregar el ID del problema al diccionario de datos
    tags = data.get("tags", "")
    if isinstance(tags, str):  # Verificamos que 'tags' es una cadena antes de procesar
        # Filtrar solo los tags no numéricos
        tags = [tag.strip() for tag in tags.split(',') if not re.match(r'^\d+$', tag.strip())]
    else:
        tags = []  # Si 'tags' no es una cadena, se deja como una lista vacía
    data['tags'] = tags  # Actualizar los tags en data
    node_data.append(data)

# Convertir los datos de nodos en un DataFrame para su análisis
df_nodes = pd.DataFrame(node_data)

# Asumimos que cada nodo tiene un atributo 'community' que identifica la comunidad de cada nodo
if 'community' not in df_nodes.columns:
    raise ValueError("Cada nodo debe tener un atributo de comunidad para este análisis.")

# Calcular el número de tags por nodo
df_nodes['num_tags'] = df_nodes['tags'].apply(len)

# Calcular la media de tags por comunidad
mean_tags_per_community = df_nodes.groupby('community')['num_tags'].mean()

# Mostrar todos los elementos del array sin truncar
pd.set_option('display.max_rows', None)

# Imprimir la media de tags por comunidad
print("Media de tags por comunidad:\n", mean_tags_per_community)

# Restaurar la configuración por defecto si lo deseas
pd.reset_option('display.max_rows')

# Contar la cantidad de nodos en cada comunidad
community_counts = df_nodes['community'].value_counts()

# Calcular estadísticas descriptivas
community_stats = community_counts.describe()
print("Estadísticas descriptivas de cantidad de elementos en cada comunidad:\n", community_stats)

# Calcular frecuencia de cada tag en cada comunidad
tag_count_by_community = (
    df_nodes.explode('tags')
    .groupby(['community', 'tags'])
    .size()
    .unstack(fill_value=0)
)

# Calcular el máximo de cada fila y comparar con el 50% del tamaño de la comunidad
majority_tags = (tag_count_by_community.T / tag_count_by_community.sum(axis=1)).T
majority_communities = majority_tags[majority_tags > 0.5].dropna(how='all')
print("Comunidades con un tag mayor a la mitad de elementos:\n", majority_communities.index.tolist())

# Identificar la comunidad con la frecuencia más alta para cada tag
top_community_for_tag = tag_count_by_community.idxmax(axis=0)
top_community_for_tag_counts = tag_count_by_community.max(axis=0)

# Imprimir elementos de cada comunidad relevante para cada tag
for tag, community in top_community_for_tag.items():
    community_nodes = df_nodes[df_nodes['community'] == community]
    print(f"Tag: {tag}\nComunidad: {community}\nCantidad: {top_community_for_tag_counts[tag]}")
    print("Elementos de la comunidad:", community_nodes['problem_id'].tolist(), "\n")

from collections import Counter, defaultdict

# Paso 1: Encontrar el tag más frecuente en cada comunidad
community_tags = defaultdict(list)
for community, group in df_nodes.groupby('community'):
    all_tags = [tag for tags in group['tags'] if tags for tag in tags]  # Asegurarse de que 'tags' no esté vacío
    if all_tags:  # Solo proceder si hay tags en esta comunidad
        tag_counts = Counter(all_tags)
        max_count = max(tag_counts.values())
        dominant_tags = [tag for tag, count in tag_counts.items() if count == max_count]
        community_tags[community] = dominant_tags

# Paso 2: Contar en cuántas comunidades aparece cada tag como el dominante
tag_dominance_counts = Counter([tag for tags in community_tags.values() for tag in tags])

# Paso 3: Encontrar tags dominantes en al menos dos comunidades
repeated_dominant_tags = {tag: count for tag, count in tag_dominance_counts.items() if count >= 2}

# Imprimir los resultados
print("Tags que son dominantes en al menos dos comunidades:")
for tag, count in repeated_dominant_tags.items():
    communities_with_tag = [community for community, tags in community_tags.items() if tag in tags]
    print(f"Tag: {tag}, Repite en {count} comunidades: {communities_with_tag}")

# Paso 1: Encontrar el tag o tags dominantes en cada comunidad
community_tags = defaultdict(list)
for community, group in df_nodes.groupby('community'):
    all_tags = [tag for tags in group['tags'] if tags for tag in tags]
    if all_tags:  # Solo proceder si hay tags en esta comunidad
        tag_counts = Counter(all_tags)
        max_count = max(tag_counts.values())
        dominant_tags = sorted([tag for tag, count in tag_counts.items() if count == max_count])
        community_tags[community] = tuple(dominant_tags)  # Guardar los tags dominantes como una tupla ordenada

# Paso 2: Contar cada combinación de tags dominantes y ver si se repite en varias comunidades
tag_pair_counts = Counter(community_tags.values())

# Paso 3: Encontrar pares de tags dominantes que se repiten en al menos dos comunidades
repeated_tag_pairs = {tags: count for tags, count in tag_pair_counts.items() if count >= 2}

# Imprimir los resultados
print("Pares de tags dominantes repetidos en múltiples comunidades:")
for tags, count in repeated_tag_pairs.items():
    communities_with_tags = [community for community, dom_tags in community_tags.items() if dom_tags == tags]
    print(f"Tags dominantes: {tags}, Repetidos en {count} comunidades: {communities_with_tags}")