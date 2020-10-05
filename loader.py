from util import connect
from dataCollector import *
from cleaners import *

def full_load():
    g_data = getGenericFPLData()
    teams = [[team['id'], team['name']] for team in g_data['teams']]
    players_fpl = g_data['elements']

    cleaned_players_fpl = [fpl_player_cleaner(player) for player in players_fpl]

    FBref_urls = [
        'https://fbref.com/en/comps/9/1631/stats/2017-2018-Premier-League-Stats',
        'https://fbref.com/en/comps/9/1889/stats/2018-2019-Premier-League-Stats',
        'https://fbref.com/en/comps/9/3232/stats/2019-2020-Premier-League-Stats',
        'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
    ]
    FBref_gk_urls = [
        'https://fbref.com/en/comps/9/1631/keepers/2017-2018-Premier-League-Stats',
        'https://fbref.com/en/comps/9/1889/keepers/2018-2019-Premier-League-Stats',
        'https://fbref.com/en/comps/9/3232/keepers/2019-2020-Premier-League-Stats',
        'https://fbref.com/en/comps/9/keepers/Premier-League-Stats']

    player_info = []

    team_data, player_data = getFBrefdata(FBref_urls[0])

    print(cleaned_players_fpl[0])
    print('')
    print(player_data[0])

    return

def update_load():
    return

full_load()