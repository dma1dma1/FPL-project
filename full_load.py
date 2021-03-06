from util import connect, csvtodicts, parsegws
from collections import defaultdict
from dataCollector import *
from cleaners import *
from constants import FBref_urls, FBref_gk_urls, gw_data, player_history

def full_load():
    '''
    Performs a first load on the database
    '''
    print("Beginning Full Load...\n")
    print("Initializing tables...\n")

    connect('SQL/drop.sql', isfile=True)
    connect('SQL/init_db.sql', isfile=True)

    print("Finished initializing tables!\n")

    g_data = getGenericFPLData()
    team_season_data = []
    player_season_data = []
    
    ## Loading team_info Database ##
    print("Loading team_info...\n")

    teams = [[team['code'], team['name']] for team in g_data['teams']]
    t_info_string = ", ".join("('%s', '%s')" % (code, name) for (code, name) in teams)
    team_info_query = """INSERT INTO team_info (team_code, team_name) VALUES""" + t_info_string
    connect(team_info_query)

    print("Finished loading team_info\n")

    ## Loading player_info Database ##
    print("Loading player_info...\n")

    players_fpl = g_data['elements']
    fpl_clean_players = [fpl_player_cleaner(player) for player in players_fpl]
    player_data_final = [(d['player_name'], d['team_code']) for d in fpl_clean_players]

    # Players currently with teams
    fpl_players = set(player_info_cleaner(player) for player in players_fpl)

    old_players = set()

    # Get FBref data
    for url, year in zip(FBref_urls, ['2017-18', '2018-19', '2019-20', '2020-21']):
        team_data, player_data = getFBrefdata(url, 'standard')
        for team in team_data:
            team['season'] = year
        for player in player_data:
            player['season'] = year
        team_season_data += team_data
        player_season_data += player_data
        old_players = old_players | (set(player_info_cleaner(player) for player in player_data) - fpl_players)

    # Update current season FPL
    for player in players_fpl:
        player['season'] = '2020-21'

    # Get FPL player data
    for f, season in zip(player_history, ['2017-18', '2018-19', '2019-20']):
        data = csvtodicts(f)
        for player in data:
            player['season'] = season
        players_fpl += data
        old_players = old_players | (set(player_info_cleaner(player) for player in data) - fpl_players)

    for player in old_players:
        if player not in fpl_players:
            player_data_final.append((player, None))

    player_info_query = """INSERT INTO player_info (player_name, team_code) VALUES (%s, %s)"""
    connect(player_info_query, data=player_data_final)

    print("Finished loading player_info\n")

    ## Loading team_season_data Database ##

    print("Loading team_season_data...\n")

    # Get team_id and team_name from previously loaded team_info database
    get_team_season_query = """SELECT team_id, team_name FROM team_info"""
    team_ids = {name:p_id for (p_id, name) in connect(get_team_season_query, hasReturn=True)}
    
    team_season_data = [team_season_cleaner(team, team_ids) for team in team_season_data]
    team_season_data = [[None if v=='' else v for v in team]for team in team_season_data]
    team_season_query = """INSERT INTO team_season_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    connect(team_season_query, data=team_season_data)

    print("Finished loading team_season_data!\n")

    ## Loading player_season_data Database ##

    print("Loading player_season_data...\n")

    # Get player_id and player_name from previously loaded player_info database
    get_info_query = """SELECT player_id, player_name FROM player_info"""
    player_ids = {name:p_id for (p_id, name) in connect(get_info_query, hasReturn=True)}

    clean_players_fpl = [fpl_player_season_cleaner(player) for player in players_fpl]
    clean_players_FBref = [FBref_player_cleaner(player) for player in player_season_data]
 
    all_player_season_data = defaultdict(lambda: defaultdict(lambda: None))

    # Combine data from both sources
    for player in clean_players_fpl:
        all_player_season_data[(player['player_name'], player['season'])].update(player)
    for player in clean_players_FBref:
        # Catch players who moved teams mid year
        if (player['player_name'], player['season']) in all_player_season_data and all_player_season_data[(player['player_name'], player['season'])]['xg'] is not None:
            for key in list(player.keys())[2:]:
                value = all_player_season_data[(player['player_name'], player['season'])][key]
                newValue = player[key]
                if value != '':
                    if newValue != '':
                        all_player_season_data[(player['player_name'], player['season'])][key] = str(float(value) + float(newValue))
                elif newValue != '':
                    all_player_season_data[(player['player_name'], player['season'])][key] = newValue
        else:
            all_player_season_data[(player['player_name'], player['season'])].update(player)

    player_season_data_final = list(all_player_season_data.values())

    for player in player_season_data_final:
        try:
            player['id'] = player_ids[player['player_name']]
        except:
            player['id'] = None

    player_season_data_final = [player_season_cleaner(player) for player in player_season_data_final]
    player_season_data_final = [[None if v=='' else v for v in player]for player in player_season_data_final]
    player_season_query = """INSERT INTO player_season_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    connect(player_season_query, data=player_season_data_final)

    print("Finished loading player_season_data!\n")

    ## Loading goalkeeper_season_data ##

    print('Loading goalkeeper_season_data...\n')

    goalie_data = []

    for url, season in zip(FBref_gk_urls, ['2017-18', '2018-19', '2019-20', '2020-21']):
        _, player_data = getFBrefdata(url, 'goalkeeping')
        for player in player_data:
            player['season'] = season
        goalie_data += player_data
    
    goalie_data = [FBref_goalie_cleaner(player) for player in goalie_data]

    for player in goalie_data:
        try: 
            player[0] = player_ids[player[0]]
        except:
            player[0] = None

    goalie_data = [[None if v=='' else v for v in player] for player in goalie_data]
    goalie_query = """INSERT INTO goalkeeper_season_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    connect(goalie_query, data=goalie_data)

    print('Finished loading goalkeeper_season_data!\n')

    ## Loading gw_player_data ##

    print('Loading gw_player_data...\n')

    fpl_player_ids = [[d['player_name'], d['id']] for d in fpl_clean_players]
    
    gw_data_final = parsegws(fpl_player_ids)

    element_types = {(player[0], player[1]):player[2] for player in player_season_data_final}

    for f, season in zip(gw_data, ['2017-18', '2018-19', '2019-20']):
        data = csvtodicts(f, encoding='latin-1')
        data = [gw_data_cleaner(player, season=season) for player in data]
        gw_data_final += data

    for player in gw_data_final:
        try:
            player['id'] = player_ids[player['player_name']]
        except:
            player['id'] = None

        try:
            player['element_type'] = element_types[(player['id'], player['season'])]
        except:
            player['element_type'] = None

    gw_data_final = [gw_player_cleaner(player) for player in gw_data_final]
    gw_data_final = [[None if v=='' else v for v in player]for player in gw_data_final]
    gw_query = """INSERT INTO gw_player_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    connect(gw_query, data=gw_data_final)

    print('Finished loading gw_player_data!\n')
    print('Full Load Finished!')

    return

if __name__ == "__main__":
    full_load()