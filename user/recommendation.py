import requests
import networkx as nx
import random
import pandas as pd  # Importar pandas para verificar NaN
from collections import defaultdict

# Función para obtener el rating actual de un usuario en Codeforces
def get_user_rating(username):
    url = f"https://codeforces.com/api/user.info?handles={username}"
    response = requests.get(url).json()
    return response['result'][0]['rating'] if response['status'] == 'OK' else None

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
                    problem_id = f"{contest_id}_{problem_index}"
                    solved_problems.add(problem_id)
    return solved_problems

# Función para recomendar problemas
def recommend_problems(username, n=5, m=5, rating_range=[100, 300]):
    user_rating = get_user_rating(username)
    if user_rating is None:
        print("Error al obtener el rating del usuario.")
        return

    solved_problems = get_user_solved_problems(username)

    # Cargar el grafo
    G_nx = nx.read_graphml("codeforces_community_graph.graphml")

    # Filtrar problemas dentro del rango de rating deseado
    candidate_problems = [
        node for node, data in G_nx.nodes(data=True)
        if 'rating' in data and isinstance(data['rating'], (int, float)) and not pd.isna(data['rating']) 
        and rating_range[0] <= int(data['rating']) - user_rating <= rating_range[1]
    ]

    # Organizar problemas por comunidad
    community_problems = defaultdict(list)
    for problem_id in candidate_problems:
        if problem_id not in solved_problems:  # Solo consideramos problemas no resueltos
            community = G_nx.nodes[problem_id].get('community')
            if community:
                community_problems[community].append(problem_id)

    # Recomendaciones de problemas en comunidades desconocidas
    unknown_community_recommendations = []
    known_community_recommendations = []
    
    # Seleccionar n comunidades que el usuario no ha resuelto
    unsolved_communities = [c for c in community_problems if not any(p in solved_problems for p in community_problems[c])]
    
    if unsolved_communities:
        for community in random.sample(unsolved_communities, min(n, len(unsolved_communities))):
            unknown_community_recommendations.extend(random.sample(community_problems[community], 1))
    
    # Seleccionar m comunidades conocidas o similares por rating
    for problem in solved_problems:
        if problem in G_nx:
            community = G_nx.nodes[problem]['community']
            if community not in known_community_recommendations:  # Evitar duplicados
                known_community_recommendations.extend(random.sample(community_problems[community], min(1, len(community_problems[community]))))

    # Si no se encuentran suficientes problemas de comunidades conocidas, buscar problemas similares
    if len(known_community_recommendations) < m:
        similar_candidates = [
            p for p in candidate_problems
            if rating_range[0] <= G_nx.nodes[p]['rating'] - user_rating <= rating_range[1] and p not in solved_problems
        ]
        random.shuffle(similar_candidates)  # Mezclar candidatos para obtener diversidad
        known_community_recommendations.extend(similar_candidates[:m - len(known_community_recommendations)])

    # Mostrar recomendaciones
    print(f"Recomendaciones para el usuario '{username}':")
    print("Problemas en comunidades nuevas:")
    for problem_id in unknown_community_recommendations:
        print(f"- {problem_id} | Rating: {G_nx.nodes[problem_id]['rating']} | URL: {G_nx.nodes[problem_id]['url']}")
    
    print("\nProblemas en comunidades conocidas:")
    for problem_id in known_community_recommendations:
        print(f"- {problem_id} | Rating: {G_nx.nodes[problem_id]['rating']} | URL: {G_nx.nodes[problem_id]['url']}")

# Ejemplo de uso
recommend_problems("racsosabe")
