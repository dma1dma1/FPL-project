from name_changes import NAME_CHANGES_20_21

def fpl_player_cleaner(player):
    first = player['first_name']
    last = player['second_name']
    element_type = player['element_type']
    team_id = player['team']
    chance_playing = player['chance_of_playing_this_round']

    return {
        'player_name': first + ' ' + last, 
        'element_type': element_type, 
        'team_id': team_id,
        'chance_playing': chance_playing}

def FBref_player_cleaner(player):
    name = player['Player']
    if name in NAME_CHANGES_20_21:
        name = NAME_CHANGES_20_21[name]
