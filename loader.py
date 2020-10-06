from util import connect, csvtodicts, debug_names
from collections import defaultdict
from dataCollector import *
from cleaners import *
from constants import FBref_urls, FBref_gk_urls, gw_data, player_history

def full_load():
    '''
    Performs a first load on the database
    '''
    #connect('SQL/init_db.sql', True)
    g_data = getGenericFPLData()
    

    # Load team_info Database
    '''teams = [[team['code'], team['name']] for team in g_data['teams']]
    t_data = ", ".join("('%s', '%s')" % (code, name) for (code, name) in teams)
    team_query = """INSERT INTO team_info (team_code, team_name) VALUES""" + t_data
    connect(team_query, isfile=False, data=teams)'''

    # Load player_info Database
    players_fpl = g_data['elements']
    player_names = [player_info_cleaner(player) for player in players_fpl]

    for url in FBref_urls:
        getFBrefdata(url, 'standard')
    


    d = defaultdict(dict)

    experiment = defaultdict(dict)

    efpl = csvtodicts(player_history[2])
    t, p = getFBrefdata(FBref_urls[2], 'standard')
    cefpl = [fpl_player_cleaner(player) for player in efpl]
    cefbref = [FBref_player_cleaner(player) for player in p]

    for player in cefpl:
        experiment[player['player_name']].update(player)
    for player in cefbref:
        experiment[player['player_name']].update(player)
    
    return

def update_load():
    return

full_load()