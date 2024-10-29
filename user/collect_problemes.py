import requests

handle = 'Bashca'
url = f'https://codeforces.com/api/user.status?handle={handle}'
response = requests.get(url)
data = response.json()

# Crear un conjunto de problemas resueltos
accepted_problems = {f"{submission['problem']['contestId']}-{submission['problem']['index']}"
                     for submission in data['result'] if submission['verdict'] == 'OK'}

# Mostrar los identificadores únicos de los problemas resueltos
for problem in sorted(accepted_problems):
    print(problem)
