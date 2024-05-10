from time import sleep
import requests

def generate(league_id, name):
    token = '4e73494656b6499db04556c316d8648c'
    league_id = int(league_id)

    url = f'https://api.football-data.org/v2/competitions/{league_id}/matches'
    headers = {'X-Auth-Token': token}
    response = requests.get(url, headers=headers)

    i = 0

    if response.status_code == 200:
        print(f'{league_id}: {name}')
        return False
        data = response.json()
        teams_info = dict()

        for match in data['matches']:
            status = match['status']
            if status == 'FINISHED':
                print(f'{i}')
                i += 1
                home_team = match['homeTeam']['name']
                away_team = match['awayTeam']['name']

                if home_team not in teams_info:
                    teams_info[home_team] = dict({'Goals For': 0, 'Goals Against': 0, 'Games Violates': 0, 'Games Violateds': 0, 'Games': 0})

                if away_team not in teams_info:
                    teams_info[away_team] = dict({'Goals For': 0, 'Goals Against': 0, 'Games Violates': 0, 'Games Violateds': 0, 'Games': 0})

                home_score = int(match['score']['fullTime']['homeTeam'])
                away_score = int(match['score']['fullTime']['awayTeam'])

                home_violate = 1 if home_score > 0 else 0
                home_violated = 1 if away_score > 0 else 0
                teams_info[home_team]['Goals For'] += home_score
                teams_info[home_team]['Goals Against'] += away_score
                teams_info[home_team]['Games Violates'] += home_violate
                teams_info[home_team]['Games Violateds'] += home_violated
                teams_info[home_team]['Games'] += 1
                
                away_violate = 1 if away_score > 0 else 0
                away_violated = 1 if home_score > 0 else 0
                teams_info[away_team]['Goals For'] += away_score
                teams_info[away_team]['Goals Against'] += home_score
                teams_info[away_team]['Games Violates'] += away_violate
                teams_info[away_team]['Games Violateds'] += away_violated
                teams_info[away_team]['Games'] += 1
            else:
                print(status)

        for team, stats in teams_info.items():
            violates = stats['Games Violates']
            violated = stats['Games Violateds']
            games = stats['Games']
            cutline = games // 7

            print(f'{team} violates {violates} times')
            print(f'{team} violated {violated} times')
            print('')

        print('')
        print('-'*50)
        print('')
        print('')

        for team, stats in teams_info.items():
            violates = stats['Games Violates']
            violated = stats['Games Violateds']
            games = stats['Games']
            cutline = games // 7

            if games - violates < cutline:
                print(f'{team} violates {violates} times')

            if 36 - violated < 5:
                print(f'{team} violated {violated} times')

# Defina o token de acesso à API
token = '4e73494656b6499db04556c316d8648c'

# Faça a solicitação GET para obter informações sobre as competições
url = 'https://api.football-data.org/v2/competitions'
headers = {'X-Auth-Token': token}
response = requests.get(url, headers=headers)

# Verifique se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Converta a resposta para JSON
    data = response.json()

    # Exiba as informações sobre as competições, incluindo seus IDs
    for competition in data['competitions']:
        generate(competition['id'], competition['name'])
else:
    print("Erro ao recuperar os dados. Status code:", response.status_code)




# 2013: Campeonato Brasileiro Série A
# 2016: Championship
# 2021: Premier League
# 2015: Ligue 1
# 2017: Primeira Liga
# 2152: Copa Libertadores