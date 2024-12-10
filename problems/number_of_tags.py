import requests
from collections import defaultdict

# URL de la API de Codeforces para obtener la lista de problemas
url = 'https://codeforces.com/api/problemset.problems'

# Realizamos una solicitud GET para obtener los problemas
response = requests.get(url)
data = response.json()

# Verificamos si la solicitud fue exitosa
if data['status'] == 'OK':
    tag_counts = defaultdict(int)  # Contador de tags
    tag_ratings = defaultdict(list)  # Lista de ratings por tag
    
    # Recorremos todos los problemas para extraer los tags y los ratings
    for problem in data['result']['problems']:
        if 'tags' in problem:
            # Si el problema tiene rating y es numérico, lo añadimos
            if 'rating' in problem and isinstance(problem['rating'], int):
                rating = problem['rating']
                for tag in problem['tags']:
                    tag_counts[tag] += 1  # Contamos el problema para el tag
                    tag_ratings[tag].append(rating)  # Añadimos el rating al tag
    
    # Mostramos los tags con su cantidad de problemas y el rating medio
    print(f"Tags disponibles en Codeforces ({len(tag_counts)}):")
    for tag, count in sorted(tag_counts.items()):
        # Calculamos el rating medio solo si hay ratings disponibles
        if tag_ratings[tag]:
            average_rating = sum(tag_ratings[tag]) / len(tag_ratings[tag])
        else:
            average_rating = 0  # Si no hay ratings, lo dejamos en 0
        print(f"{tag}: {count} problemas, Rating medio: {average_rating:.2f}")
else:
    print("Error al obtener datos de Codeforces.")
