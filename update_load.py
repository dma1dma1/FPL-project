from util import connect, getGameweek
from collections import defaultdict
from dataCollector import *
from cleaners import *
from constants import FBref_urls, FBref_gk_urls, gw_data, player_history

def update_load():
    '''
    Updates tables in database
    '''
    print("Beginning update...\n")

    ## Update team_info database ##

    print("Updating team_info...\n")

    g_data = getGenericFPLData()
    teams = set((team['code'], team['name']) for team in g_data['teams'])

    # Get existing teams
    old_teams = set(connect("""SELECT team_code, team_name FROM team_info""", hasReturn=True))

    team_diff = teams - old_teams
    if len(team_diff) > 0:
        t_info_string = ", ".join("('%s', '%s')" % (code, name) for (code, name) in team_diff)
        team_info_query = """INSERT INTO team_info (team_code, team_name) VALUES""" + t_info_string
        connect(team_info_query)
        print("Finished updating team_info!\n")
    else:
        print("No updates needed!\n")

    ## Update player_info database ##
    
    print("Updating player_info...\n")

    players_fpl = g_data['elements']
    fpl_clean_players = [fpl_player_cleaner(player) for player in players_fpl]
    current_player_info = set((d['player_name'], d['team_code']) for d in fpl_clean_players)
    current_players = set(player_info_cleaner(player) for player in players_fpl)

    # Get existing players
    old_player_teams = set(connect("""SELECT player_name, team_code FROM player_info WHERE team_code IS NOT NULL""", hasReturn=True))
    old_players = set(player[0] for player in connect("""SELECT player_name FROM player_info""", hasReturn=True))

    # Check for changes
    player_diff_new = current_player_info - old_player_teams
    player_diff_old = old_player_teams - current_player_info

    # New players


    # Players who changed teams
    updates = []

    # Players who left teams
    team_removals = []

    for player in player_diff_new:
        pass   

    return

if __name__ == "__main__":
    update_load()