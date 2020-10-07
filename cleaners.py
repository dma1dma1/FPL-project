from name_changes import NAME_CHANGES

def nameCleaner(name):
    '''
    This function cleans a name to be standardized, and ready for insertion into SQL
    '''
    if name in NAME_CHANGES:
        name = NAME_CHANGES[name]
    return name.replace("'", "''")

def player_info_cleaner(player):
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
        'team_code': player['team_code'],
        'chance_playing': player['chance_of_playing_this_round']}

def FBref_player_cleaner(player):
    name = nameCleaner(player['Player'])
    return {
        'player_name': name,
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

def gw_data_cleaner(player):
    name = ' '.join((player['name'].split('_'))[:2])
    player['player_name'] = name
    del player['name']
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