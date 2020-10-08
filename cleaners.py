from name_changes import NAME_CHANGES

def nameCleaner(name):
    '''
    Cleans a name to be standardized, and ready for insertion into SQL
    '''
    if name in NAME_CHANGES:
        name = NAME_CHANGES[name]
    return name.replace("'", "''")

def player_info_cleaner(player):
    '''
    Extracts name from both FPL and FBref players
    '''
    name = ''

    # FPL data
    try: 
        name = player['first_name'] + ' ' + player['second_name']
    except:
        # FBref data
        try:
            name = player['Player']
        except:
            print(player, 'No name found')
   
    return nameCleaner(name)

def fpl_player_cleaner(player):
    name = nameCleaner(player['first_name'] + ' ' + player['second_name'])
    return {
        'player_name': name, 
        'element_type': player['element_type'], 
        'id': player['id'],
        'team_code': player['team_code']
    }

def fpl_player_season_cleaner(player):
    name = nameCleaner(player['first_name'] + ' ' + player['second_name'])
    return {
        'player_name': name,
        'season': player['season'],
        'element_type': player['element_type'],
        'start_cost': str(int(player['now_cost']) - int(player['cost_change_start'])),
        'end_cost': player['now_cost'],
        'total_points': player['total_points'],
        'minutes': player['minutes'],
        'goals_scored': player['goals_scored'],
        'assists': player['assists'],
        'clean_sheets': player['clean_sheets'],
        'goals_conceded': player['goals_conceded'],
        'own_goals': player['own_goals'],
        'penalties_saved': player['penalties_saved'],
        'penalties_missed': player['penalties_missed'],
        'yellow_cards': player['yellow_cards'],
        'red_cards': player['red_cards'],
        'saves': player['saves'],
        'bonus': player['bonus'],
        'bps': player['bps'],
        'influence': player['influence'],
        'creativity': player['creativity'],
        'threat': player['threat'],
        'ict_index': player['ict_index']
    }

def FBref_player_cleaner(player):
    name = nameCleaner(player['Player'])
    return {
        'player_name': name,
        'season': player['season'],
        'gls_90': player['Gls_90'],
        'ast_90': player['Ast_90'],
        'g+a_90': player['G+A_90'],
        'g-pk_90': player['G-PK_90'],
        'g+a-pk_90': player['G+A-PK_90'],
        'xg': player['xG'],
        'npxg': player['npxG'],
        'xa': player['xA'],
        'xg_90': player['xG_90'],
        'xa_90': player['xA_90'],
        'xg+xa_90': player['xG+xA_90'],
        'npxg_90': player['npxG_90'],
        'npxg+xa_90': player['npxG+xA_90']
    }

def gw_data_cleaner(player, season = None):
    name = ' '.join((player['name'].split('_'))[:2])
    player['player_name'] = nameCleaner(name)
    del player['name']
    if season:
        player['season'] = season
    return player

def team_season_cleaner(team):
    return [
        team['id'],
        team['Squad'],
        team['season'],
        team['Gls'],
        team['Ast'],
        team['PK'],
        team['PKatt'],
        team['CrdY'],
        team['CrdR'],
        team['Gls_90'],
        team['Ast_90'],
        team['G+A_90'],
        team['G-PK_90'],
        team['G+A-PK_90'],
        team['xG'],
        team['npxG'],
        team['xA'],
        team['xG_90'],
        team['xA_90'],
        team['xG+xA_90'],
        team['npxG_90'],
        team['npxG+xA_90']
    ]

def player_season_cleaner(player):
    return [
        player['id'],
        player['season'],
        player['element_type'],
        player['start_cost'],
        player['end_cost'],
        player['total_points'],
        player['minutes'],
        player['goals_scored'],
        player['assists'],
        player['clean_sheets'],
        player['goals_conceded'],
        player['own_goals'],
        player['penalties_saved'],
        player['penalties_missed'],
        player['yellow_cards'],
        player['red_cards'],
        player['saves'],
        player['bonus'],
        player['bps'],
        player['influence'],
        player['creativity'],
        player['threat'],
        player['ict_index'],
        player['gls_90'],
        player['ast_90'],
        player['g+a_90'],
        player['g-pk_90'],
        player['g+a-pk_90'],
        player['xg'],
        player['npxg'],
        player['xg'],
        player['xg_90'],
        player['xa_90'],
        player['xg+xa_90'],
        player['npxg_90'],
        player['npxg+xa_90']
    ]

def FBref_goalie_cleaner(player):
    name = nameCleaner(player['Player'])
    return [
        name,
        player['season'],
        player['GA'],
        player['GA90'],
        player['SoTA'],
        player['Saves'],
        player['Save%'],
        player['CS'],
        player['CS%'],
        player['PKsv']
    ]

def gw_player_cleaner(player):
    return [
        player['id'],
        player['season'],
        player['element_type'],
        player['element'],
        player['fixture'],
        player['opponent_team'],
        player['total_points'],
        player['was_home'],
        player['kickoff_time'],
        player['team_h_score'],
        player['team_a_score'],
        player['round'],
        player['minutes'],
        player['goals_scored'],
        player['assists'],
        player['clean_sheets'],
        player['goals_conceded'],
        player['own_goals'],
        player['penalties_saved'],
        player['penalties_missed'],
        player['yellow_cards'],
        player['red_cards'],
        player['saves'],
        player['bonus'],
        player['bps'],
        player['influence'],
        player['creativity'],
        player['threat'],
        player['ict_index'],
        player['value'],
        player['transfers_balance'],
        player['selected'],
        player['transfers_in'],
        player['transfers_out'],
        player['GW'],
    ]