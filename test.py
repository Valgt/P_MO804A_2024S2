import csv
import requests

# Definir la URL de la API para obtener la lista de problemas
url = "https://codeforces.com/api/problemset.problems"

# Realizar la solicitud
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()
    problems = data['result']['problems']
    problem_statistics = data['result']['problemStatistics']

    # Crear el archivo CSV
    csv_file = 'codeforces_problems.csv'
    
    # Definir los encabezados del archivo CSV
    headers = ['Contest ID', 'Problem Index', 'Name', 'Type', 'Points', 'Tags', 'Solved Count', 'Rating']

    # Abrir el archivo en modo de escritura con codificación UTF-8
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Escribir los encabezados
        writer.writerow(headers)
        
        # Escribir los datos de cada problema
        for i, problem in enumerate(problems):
            contest_id = problem.get('contestId', 'N/A')
            index = problem.get('index', 'N/A')
            name = problem.get('name', 'N/A')
            type_ = problem.get('type', 'N/A')
            points = problem.get('points', 'N/A')
            tags = ', '.join(problem.get('tags', []))
            solved_count = problem_statistics[i].get('solvedCount', 'N/A')
            rating = problem.get('rating', 'N/A')
            
            writer.writerow([contest_id, index, name, type_, points, tags, solved_count, rating])
            
    print(f"CSV file created: {csv_file}")
else:
    print("Error en la consulta:", response.status_code)
