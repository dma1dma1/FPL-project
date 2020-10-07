from util import connect, csvtodicts, debug_names
from collections import defaultdict
from dataCollector import *
from cleaners import *
from constants import FBref_urls, FBref_gk_urls, gw_data, player_history

def full_load():
    '''
    Performs a first load on the database
    '''
    print("Initializing tables...\n")

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

    for url, year in zip(FBref_urls, ['2017-18', '2018-19', '2019-20', '2020-21']):
        team_data, player_data = getFBrefdata(url, 'standard')
        for team in team_data:
            team['season'] = year
        for player in player_data:
            player['season'] = year
        team_season_data += team_data
        player_season_data += player_data
        old_players = old_players | (set(player_info_cleaner(player) for player in player_data) - fpl_players)

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
    team_ids = {name:id for (id, name) in connect(get_team_season_query, hasReturn=True)}

    for team in team_season_data:
        try:
            team['id'] = team_ids[team['Squad']]
        except:
            team['id'] = None
    
    team_season_data = [team_season_cleaner(team) for team in team_season_data]
    team_season_data = [[None if v=='' else v for v in team]for team in team_season_data]
    team_season_query = """INSERT INTO team_season_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    connect(team_season_query, data=team_season_data)

    print("Finished loading team_season_data!\n")

    ## Loading player_season_data Database ##

    print("Loading player_season_data...\n")

    # Get player_id and player_name from previously loaded player_info database
    get_info_query = """SELECT player_name, team_code FROM player_info"""
    player_ids = connect(get_info_query, hasReturn=True)

    '''experiment = defaultdict(dict)

    efpl = g_data['elements']
    t, p = getFBrefdata(FBref_urls[3], 'standard')
    cefpl = [fpl_player_cleaner(player) for player in efpl]
    cefbref = [FBref_player_cleaner(player) for player in p]

    for player in cefpl:
        experiment[player['player_name']].update(player)
    for player in cefbref:
        experiment[player['player_name']].update(player)'''
    
    return

def update_load():
    return

full_load()