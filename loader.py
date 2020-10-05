from util import connect, csvtodicts, debug_names
from collections import defaultdict
from dataCollector import *
from cleaners import fpl_player_cleaner, FBref_player_cleaner, gw_data_cleaner
from constants import FBref_urls, FBref_gk_urls, gw_data, player_history

def full_load():
    '''g_data = getGenericFPLData()
    teams = [[team['id'], team['name']] for team in g_data['teams']]
    players_fpl = g_data['elements']

    cleaned_players_fpl = [fpl_player_cleaner(player) for player in players_fpl]    

    team_data, player_data = getFBrefdata(FBref_urls[3], 'standard')
    clean_player_data = [FBref_player_cleaner(player) for player in player_data]

    d = defaultdict(dict)'''

    experiment = defaultdict(dict)

    efpl = csvtodicts(player_history[0])
    t, p = getFBrefdata(FBref_urls[0], 'standard')
    cefpl = [fpl_player_cleaner(player) for player in efpl]
    cefbref = [FBref_player_cleaner(player) for player in p]

    for player in cefpl:
        experiment[player['player_name']].update(player)
    for player in cefbref:
        experiment[player['player_name']].update(player)
    
    debug_names(experiment)
    return

def update_load():
    return

full_load()