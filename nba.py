from sys import exit
from datetime import datetime
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import re

def create_columns(dictionary, list, opponent_performance):
    for value in list:
        minus_column = f'-{value}'
        plus_column = f'+{value}'
        minus_home = f'HOME {minus_column}'
        plus_home = f'HOME {plus_column}'
        minus_away = f'AWAY {minus_column}'
        plus_away = f'AWAY {plus_column}'    

        dictionary[minus_home] = 0
        dictionary[minus_away] = 0
        dictionary[plus_home] = 0
        dictionary[plus_away] = 0

        if opponente_performance:
            dictionary[f'OPPONENT {minus_home}'] = 0
            dictionary[f'OPPONENT {minus_away}'] = 0
            dictionary[f'OPPONENT {plus_home}'] = 0
            dictionary[f'OPPONENT {plus_away}'] = 0

    return dictionary

def generate_values(team, points, at, columns):
    for column in columns:
        column_name = f'{at} {column}'
        plus_name = column_name.replace(' ', ' +')
        minus_name = column_name.replace(' ', ' -')

        comparison = float(column)
        if points > comparison:
            team[plus_name] += 1
        
        if points < comparison:
            team[minus_name] += 1

    return team

def generate_unique_values(team, points, at, columns, opponent = False):
    for column in columns:
        if opponent:
            column_name = f'OPPONENT {at} {column}'
        else:
            column_name = f'{at} {column}'
        
        # plus_name = column_name.replace(' ', ' +')
        # minus_name = column_name.replace(' ', ' -')
        plus_name = re.sub(r'\s(\d+\.?\d*)', r' +\1', column_name)
        minus_name = re.sub(r'\s(\d+\.?\d*)', r' -\1', column_name)

        comparison = float(column)
        if points > comparison:
            team[plus_name] += 1
        
        if points < comparison:
            team[minus_name] += 1
        


    return team


team_name = input('Digite o nome do time: ')

while(True):
    print('1. HOME')
    print('2. AWAY')
    mando = input('Digite o mando: ')
    mando = int(mando)

    if mando == 1:
        mando = 'HOME'
        break
    elif mando == 2:
        mando = 'AWAY'
        break

print('')

while(True):
    print('1. VALORES COMBINADOS')
    print('2. VALORES ÚNICOS')

    tipo = input('Digite o mando: ')
    tipo = int(tipo)

    if(tipo == 1 or tipo == 2):
        break

print('')

if tipo == 2:
    while(True):
        print('1. SIM')
        print('2. NÃO')

        opponente_performance = input('Quer ver a performance do oponente? ')
        tipo = int(tipo)

        if(tipo == 1 or tipo == 2):
            break
else:
    opponente_performance = False



odd_range = input('Range inicio: ')

# Obtém o ID de um time específico (por exemplo, o Los Angeles Lakers)
teams_dict = teams.get_teams()
lakers = [team for team in teams_dict if team['full_name'] == team_name][0]
lakers_id = lakers['id']

# Encontrar todos os jogos da temporada regular para o Los Angeles Lakers
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=lakers_id, season_nullable='2023-24', season_type_nullable='Regular Season')
lakers_games = gamefinder.get_data_frames()[0]


time_1 = dict()

if odd_range != '':
    start = int(odd_range) - 2
    end = int(odd_range) + 7
    combined_columns = []
    
    for number in range(start, end):
        combined_columns.append(number + 0.5)

else:
    combined_columns = ['190.5', '195.5', '196.5', '197.5', '198.5', '199.5', '200.5', '201.5', '202.5', '203.5', '204.5', '205.5', '206.5', '207.5', '208.5', '209.5', '210.5', '211.5', '212.5', '213.5', '214.5', '215.5', '216.5', '217.5', '218.5', '219.5', '220.5', '221.5', '222.5', '223.5', '224.5', '225.5', '226.5', '227.5', '228.5', '229.5', '230.5', '231.5', '232.5', '233.5', '234.5', '235.5', '240.5']

time_1 = create_columns(time_1, combined_columns, opponente_performance)

i = 0
home_games = 0
away_games = 0
for index, game_info in lakers_games.iterrows():
    game = game_info["MATCHUP"]
    plus = int(game_info['PLUS_MINUS'])
    points = int(game_info['PTS'])


    if "@" not in game:
        at = 'HOME'
        op_at = 'AWAY'
        home_games += 1
    else:
        at = 'AWAY'
        op_at = 'HOME'
        away_games += 1

    if plus > 0:
        game_result = (points - plus) + points
        opponent_points = points - plus
    else:
        game_result = (points + plus) + points
        opponent_points = points + plus

    if tipo == 1:
        time_1 = generate_values(time_1, game_result, at, combined_columns)
    else:
        time_1 = generate_unique_values(time_1, points, at, combined_columns)
        time_1 = generate_unique_values(time_1, opponent_points, op_at, combined_columns, True)

ajust_home = int(home_games // 7)
ajust_away = int(away_games // 7)

for key, value in time_1.items():
    if 'HOME' in key:
        result = home_games - value
        if result < ajust_home:
            print(f'{key.upper()}: {value}')
    elif 'AWAY' in key:
        result = away_games - value
        if result < ajust_away:
            print(f'{key.upper()}: {value}')

print('')
print('-'*50)
print('')

print('HOME GAMES: ' + str(home_games))
print('AWAY GAMES: ' + str(away_games))
print('-' * 50)


for key, value in time_1.items():
    if odd_range == '' and mando in key:
        print(f'{key.upper()}: {value}')
    else:
        if 'OPPONENT' in key:
            if value > 30 and mando not in key:
                print(f'{key.upper()}: {value}')

            if value < 10 and mando not in key:
                print(f'{key.upper()}: {value}')
        else:
            if value > 30 and mando in key:
                print(f'{key.upper()}: {value}')

            if value < 10 and mando in key:
                print(f'{key.upper()}: {value}')