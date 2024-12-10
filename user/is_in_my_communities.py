import re
import requests
import networkx as nx
import random
import pandas as pd  # Importar pandas para verificar NaN
from collections import defaultdict

# Función para extraer el id del problema desde un URL
def extract_problem_id_from_url(url):
    match = re.search(r"contest/(\d+)/problem/([A-Z]\d?)", url)
    if match:
        contest_id, problem_index = match.groups()
        return f"{contest_id}-{problem_index}"
    else:
        print("URL no válido.")
        return None

# Función para obtener los problemas resueltos por un usuario
def get_user_solved_problems(username):
    url = f"https://codeforces.com/api/user.status?handle={username}"
    response = requests.get(url).json()
    solved_problems = set()
    if response['status'] == 'OK':
        for submission in response['result']:
            problem = submission.get('problem')
            if submission['verdict'] == 'OK' and problem is not None:
                contest_id = problem.get('contestId')
                problem_index = problem.get('index')
                if contest_id is not None and problem_index is not None:
                    problem_id = f"{contest_id}-{problem_index}"
                    solved_problems.add(problem_id)
    return solved_problems

# Función para verificar si un problema pertenece a alguna comunidad del usuario
def check_problem_community(username, problem_url):
    problem_id = extract_problem_id_from_url(problem_url)
    print(problem_id)
    if not problem_id:
        print("No se pudo extraer el ID del problema.")
        return

    # Cargar el grafo
    G_nx = nx.read_graphml("codeforces_community_graph.graphml")

    # Verificar si el problema está en el grafo
    if problem_id in G_nx:
        problem_community = G_nx.nodes[problem_id].get('community', None)
        print(problem_community)
        solved_problems = get_user_solved_problems(username)
        user_communities = {G_nx.nodes[p].get('community') for p in solved_problems if p in G_nx}

        if problem_community in user_communities:
            print(f"El problema '{problem_id}' pertenece a una comunidad que ya has resuelto.")
        else:
            print(f"El problema '{problem_id}' pertenece a una comunidad nueva para ti.")
    else:
        print(f"El problema '{problem_id}' no se encuentra en el grafo.")

# Ejemplo de uso
urls = []
n = int(input())
for i in range(n):
    url = input()
    urls.append(url)

for url in urls:
    check_problem_community("cegax", url)

