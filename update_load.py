from util import connect, getGameweek, parsegws
from collections import defaultdict
from dataCollector import *
from cleaners import *
from constants import FBref_urls, FBref_gk_urls, gw_data, player_history, CURRENT_SEASON

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
    old_player_info = set(connect("""SELECT player_name, team_code FROM player_info WHERE team_code IS NOT NULL""", hasReturn=True))
    old_players = set(player[0] for player in connect("""SELECT player_name FROM player_info""", hasReturn=True))

    # New players and players that changed teams
    players_changes = list(current_player_info - old_player_info)

    # Players who left teams
    players_left = old_player_info - current_player_info

    for player in players_left:
        if player[0] not in current_players:
            players_changes.append((player[0], None))

    if len(players_changes) > 0:
        players_update_query = """
        INSERT INTO player_info (player_name, team_code) VALUES (%s, %s) 
        ON CONFLICT (player_name) DO UPDATE SET team_code = EXCLUDED.team_code;"""
        connect(players_update_query, data=players_changes)
        print("Finished updating player_info!\n")
    else:
        print("No updates needed!\n")

    ## Updating team_season_data database ##

    print("Updating team_season_data...\n")

    # Get team_id and team_name from team_info database
    get_team_season_query = """SELECT team_id, team_name FROM team_info"""
    team_ids = {name:p_id for (p_id, name) in connect(get_team_season_query, hasReturn=True)}

    # Get FBref data #
    team_data, player_data = getFBrefdata(FBref_urls[-1], 'standard')
    for team in team_data:
        team['season'] = CURRENT_SEASON
    for player in player_data:
        player['season'] = CURRENT_SEASON

    team_season_data = [team_season_cleaner(team, team_ids) for team in team_data]
    team_season_data = [[None if v=='' else v for v in team]for team in team_season_data]
    team_update_season_data = [team + [team[0], team[2]] for team in team_season_data]
    team_season_update_query = """
    UPDATE team_season_data
    SET (team_id, team_name, season, goals, assists, pks, pkatts, yellow_cards, red_cards, "gls_90", "ast_90", "g+a_90", "g-pk_90", "g+a-pk_90", xg, npxg, xa, "xg_90", "xa_90", "xg+xa", "npxg_90", "npxg+xa_90") = 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    WHERE team_id = %s and season = %s
    """
    connect(team_season_update_query, data=team_update_season_data)

    print("Finished updating team_season_data!\n")

    ## Update player_season_data database ##

    print("Updating player_season_data...\n")

    # Get player_id and player_name from player_info database
    get_info_query = """SELECT player_id, player_name FROM player_info"""
    player_ids = {name:p_id for (p_id, name) in connect(get_info_query, hasReturn=True)}

    # Update current season FPL
    for player in players_fpl:
        player['season'] = '2020-21'

    clean_players_fpl = [fpl_player_season_cleaner(player) for player in players_fpl]
    clean_players_FBref = [FBref_player_cleaner(player) for player in player_data]

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
    player_season_update_data = [player + player[:2] + player for player in player_season_data_final]
    player_season_update_query = """
    WITH upsert AS (
        UPDATE player_season_data
        SET (player_id, season, element_type, start_cost, end_cost, total_points, minutes, goals_scored, assists, clean_sheets,
        goals_conceded, own_goals, penalties_saved, penalties_missed, yellow_cards, red_cards, saves, bonus, bps, influence, creativity, 
        threat, ict_index, "gls_90", "ast_90", "g+a_90", "g-pk_90", "g+a-pk_90", xg, npxg, xa, "xg_90", "xa_90", "xg+xa_90", "npxg_90", "npxg+xa_90") =
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        WHERE player_id = %s and season = %s
        RETURNING *
    )
    INSERT INTO player_season_data 
    SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s 
    WHERE NOT EXISTS (SELECT * FROM upsert)
    """
    connect(player_season_update_query, data=player_season_update_data)

    print('Finshed updating player_season_data!\n')

    ## Update goalkeeper_season_data ##

    print('Updating player_season_data...\n')

    _, goalie_data = getFBrefdata(FBref_gk_urls[-1], 'goalkeeping')
    for player in goalie_data:
        player['season'] = CURRENT_SEASON

    goalie_data = [FBref_goalie_cleaner(player) for player in goalie_data]

    for player in goalie_data:
        try: 
            player[0] = player_ids[player[0]]
        except:
            player[0] = None

    goalie_data = [[None if v=='' else v for v in player] for player in goalie_data]
    goalie_data = [player + player[:2] + player for player in goalie_data]
    goalie_update_query = """
    WITH upsert AS (
        UPDATE goalkeeper_season_data
        SET (player_id, season, goals_against, ga90, shots_against, saves, save_percent, clean_sheets, cs_percent, pks_saved) = 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        WHERE player_id = %s and season = %s
        RETURNING *
    )
    INSERT INTO goalkeeper_season_data
    SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    WHERE NOT EXISTS (SELECT * FROM upsert)
    """
    connect(goalie_update_query, data=goalie_data)

    print('Finished updating goalkeeper_season_data!\n')

    ## Update gw_player_data database ##

    print('Updating gw_player_data...\n')

    gw = getGameweek()

    fpl_player_ids = [[d['player_name'], d['id']] for d in fpl_clean_players]

    gw_data_final = parsegws(fpl_player_ids, gameweek=gw)

    element_types = {(player[0], player[1]):player[2] for player in player_season_data_final}

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
    gw_data_final = [player + player[:2] + player[-1:] + player for player in gw_data_final]
    gw_update_query = """
    WITH upsert AS (
        UPDATE gw_player_data
        SET (player_id, season, element_type, element, fixture, opponent_team, total_points, was_home, kickoff_time, team_h_score, team_a_score,
        round, minutes, goals_scored, assists, clean_sheets, goals_conceded, own_goals, penalties_saved, penalties_missed, yellow_cards, red_cards,
        saves, bonus, bps, influence, creativity, threat, ict_index, value, transfers_balance, selected, transfers_in, transfers_out, gw) =
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        WHERE player_id = %s AND season = %s AND gw = %s
        RETURNING *
    )
    INSERT INTO gw_player_data
    SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    WHERE NOT EXISTS (SELECT * FROM upsert)
    """
    connect(gw_update_query, data=gw_data_final)

    return

if __name__ == "__main__":
    update_load()