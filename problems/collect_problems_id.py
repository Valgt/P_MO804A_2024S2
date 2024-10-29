import requests
import csv

# URL para obtener todos los problemas de Codeforces
url = 'https://codeforces.com/api/problemset.problems'
response = requests.get(url)
data = response.json()

# Abrir un archivo CSV para escribir los datos
with open('codeforces_problems.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Escribir la cabecera del CSV
    writer.writerow(['Problem ID', 'Tags', 'Description', 'Rating', 'Problem URL'])
    
    # Recorrer todos los problemas
    for problem in data['result']['problems']:
        # Obtener los campos necesarios
        problem_id = f"{problem['contestId']}-{problem['index']}"
        tags = ', '.join(problem['tags'])
        description = problem['name']
        rating = problem.get('rating', 'N/A')  # Si no hay rating, usar 'N/A'
        
        # Generar la URL del problema
        problem_url = f"https://codeforces.com/contest/{problem['contestId']}/problem/{problem['index']}"
        
        # Escribir la fila en el CSV
        writer.writerow([problem_id, tags, description, rating, problem_url])

print("Archivo CSV creado con URLs de los problemas.")
