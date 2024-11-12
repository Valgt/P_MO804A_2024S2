import numpy as np
from .embedder import VectorDB
from collections import defaultdict
from tqdm.auto import tqdm
import csv
import os

# Función para extraer el identificador simplificado
def extraer_identificador(ruta):
    """
    Extrae el identificador simplificado de una ruta de archivo.
    Por ejemplo, de 'problems/414-E.json' extrae '414-E'.
    """
    try:
        # Obtener la parte después de '/' y antes de '.'
        nombre_archivo = ruta.split('/')[-1].split('.')[0]
        return nombre_archivo
    except Exception as e:
        print(f"Error al extraer el identificador de la ruta '{ruta}': {e}")
        return None

# Cargamos la base de datos de embeddings desde el archivo
db = VectorDB()
db.load_all()  # Asegúrate de que los embeddings ya estén cargados correctamente

print("Total embeddings: ", len(db.arr))
print("Total metadata: ", len(db.metadata))

# Verificar si hay duplicados en la metadata con identificadores simplificados
metadata_count = defaultdict(int)
identificadores = []

for metadata in db.metadata:
    identificador = extraer_identificador(metadata[0])
    if identificador:
        metadata_count[identificador] += 1
        identificadores.append(identificador)
    else:
        identificadores.append(None)

print("Problemas con duplicados en metadata simplificada:")
for identificador, count in metadata_count.items():
    if count != 2:  # Según tu descripción, esperas exactamente 2 ocurrencias
        print(f"'{identificador}' tiene {count} ocurrencias")

# Reemplazar la metadata original con los identificadores simplificados
# Filtrar para mantener solo los registros con identificadores válidos
db.metadata = [
    (ident, source, length) 
    for ident, (ident, source, length) in zip(identificadores, db.metadata) 
    if ident
]

print("Primer metadata simplificada:", extraer_identificador(db.metadata[0][0]))
print("Último metadata simplificada:", extraer_identificador(db.metadata[-1][0]))
print("Identificadores únicos:", len(set([x[0] for x in db.metadata])))



# Inicializar el diccionario para almacenar las similitudes
# Usaremos un diccionario con llaves ordenadas para evitar duplicados (A, B) y (B, A)
similarity_dict = {}

# Definir el rango de embeddings a procesar
# Actualmente está limitado a los primeros 100 para pruebas
# Cambia db.arr[0:100] a db.arr para procesar todos los embeddings
for idx in tqdm(range(len(db.arr)), desc="Procesando embeddings"):
    embedding = db.arr[idx]
    
    # Obtener las similitudes más cercanas
    top_similar = db.query_nearest(embedding, k=1000)
    
    # Obtener el metadata del problema actual
    current_metadata = db.metadata[idx]
    current_id = extraer_identificador(current_metadata[0])  # Identificador simplificado, e.g., '414-E'
    
    for similarity, similar_idx in top_similar:
        similar_metadata = db.metadata[similar_idx]
        similar_id = extraer_identificador(similar_metadata[0])
        
        # Crear una llave ordenada para evitar duplicados
        if current_id == similar_id:
            continue  # Evitar que un problema se compare consigo mismo
        
        pair = tuple(sorted([current_id, similar_id]))
        
        # Actualizar el diccionario con la mayor similitud
        if pair not in similarity_dict or similarity > similarity_dict[pair]:
            similarity_dict[pair] = similarity

# Verificar si el archivo CSV ya existe y eliminarlo para evitar duplicados
csv_filename = "similarity_dict.csv"
if os.path.exists(csv_filename):
    os.remove(csv_filename)

# Guardar las similitudes en un archivo CSV con filtro de similitud ≥ 0.80
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Escribir la cabecera
    csv_writer.writerow(['id1', 'id2', 'similarity'])
    
    # Escribir cada par de identificadores y su similitud si cumple con el filtro
    for (id1, id2), similarity in similarity_dict.items():
        if similarity >= 0.80:  # Filtro de similitud ≥ 0.80
            csv_writer.writerow([id1, id2, similarity])

print(f"Similitudes calculadas y guardadas en '{csv_filename}' con similitud ≥ 0.80.")