import csv
import time
import requests
from bs4 import BeautifulSoup

# Función para obtener el enunciado del problema desde la URL
def get_problem_statement(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Verificar si la página fue obtenida correctamente
        if response.status_code != 200:
            return f"Error: Unable to retrieve page, status code {response.status_code}"
        
        # Parsear el HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar el enunciado en la clase 'problem-statement'
        statement_div = soup.find('div', class_='problem-statement')
        
        if statement_div:
            return statement_div.get_text(strip=True)
        else:
            return "No statement found."
    
    except Exception as e:
        return f"Error: {str(e)}"

# Leer el archivo CSV con las URLs
with open('codeforces_problems.csv', mode='r', encoding='utf-8') as input_file, open('codeforces_problems_with_statements.csv', mode='w', newline='', encoding='utf-8') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    
    # Leer y escribir las cabeceras
    headers = next(reader)
    writer.writerow(headers + ['Statement'])
    
    # Procesar cada fila
    for row in reader:
        problem_url = row[4]  # Columna que contiene la URL
        
        # Obtener el enunciado (statement) con scraping
        statement = get_problem_statement(problem_url)
        
        # Escribir la fila original más el enunciado en el nuevo CSV
        writer.writerow(row + [statement])
        
        # Pausa para no ser detectados (2 segundos entre solicitudes)
        time.sleep(1.2)

print("Scraping completado y guardado en 'codeforces_problems_with_statements.csv'.")
