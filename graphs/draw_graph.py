import networkx as nx
import pygraphviz as pgv

# Cargar el archivo .graphml
G = nx.read_graphml("codeforces_community_graph_2.graphml")

# Convertir el grafo en formato Graphviz para optimizar el renderizado
A = nx.nx_agraph.to_agraph(G)

# Opciones para mejorar la visualización (ajustar según sea necesario)
A.graph_attr.update(size="100,100", dpi="300")  # Controla el tamaño y resolución
A.draw("graph_image.png", prog="sfdp", format="png")  # 'sfdp' es eficiente para grandes grafos


#mika_uwu: 75% de acierto 
