import psycopg2
from config import config
from dataCollector import getGenericFPLData, getPlayerFPLData
from datetime import datetime
from cleaners import nameCleaner
import csv
import time

def connect(command, hasReturn=False, isfile = False, data = None):
    '''
    Connects to postgreSQL database and runs given command

    Param:
        command (str): SQL file to be executed
        hasReturn (bool): Whether the command has a return value
        isfile (bool): Whether the command is stored in a file
        data: data to be processed

    Return:
        None
    '''
    res = None
    try:
        # Get connection params
        params = config()

        # Connect to PostgreSQL
        print('Connecting to PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print('Connected!')

        # Create cursor
        cur = conn.cursor()

        # Executing command
        print('Executing command...')
        if isfile:
            with open(command, 'r') as c:
                if data:
                    cur.executemany(c.read(), data)
                else:
                    cur.execute(c.read())
        else:
            if data:
                cur.executemany(command, data)
            else:
                cur.execute(command)
        print('Finished executing!')

        if hasReturn:
            res = cur.fetchall()

        # Close connection
        cur.close()

        # Commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            cur.close()
            conn.close()

    return res if hasReturn else None

def csvtodicts(filename, encoding='utf-8'):
    '''
    Reads a file into a list of dicts with latin-1 encoding
    '''
    with open(filename, 'r', encoding=encoding) as f:
        return list(csv.DictReader(f))

def getGameweek():
    '''
    Gets previous gameweek number
    '''
    g_data = getGenericFPLData()
    deadlines = [event['deadline_time'] for event in g_data['events']]

    # Get current time
    time = datetime.utcnow()

    # Convert deadlines to datetime while comparing
    for i in range(len(deadlines)):
        if datetime.strptime(deadlines[i], '%Y-%m-%dT%H:%M:%SZ') > time:
            return i
    return None

def parsegws(player_list, gameweek = None):
    '''
    Gets and parses past gws from this FPL season
    '''
    res = []
    for player, p_id in player_list:
        _, past_gws = getPlayerFPLData(p_id=p_id)
        if gameweek:
            # Check if data exists and most recent data is from most recent gw
            try:
                data = past_gws[-1]
                print(p_id)
                if data['round'] == gameweek:
                    data['season'] = '2020-21'
                    data['player_name'] = player
                    data['GW'] = gameweek
                    res.append(data)
            except:
                pass
        else:
            for gw in past_gws:
                gw['season'] = '2020-21'
                gw['player_name'] = player
                gw['GW'] = gw['round']
                res.append(gw)
        #time.sleep(1)
    return res
            

def debug_names(player_dict):
    print('Wrong FPL name or no FPL data: ')
    for player in player_dict.values():
        try:
            player['element_type']
        except:
            print(player['player_name'])
    '''print('')
    print('No FBref data: ')
    for player in player_dict.values():
        try:
            player['gls_90']
        except:
            print(player['player_name'])'''
    return

def getChancePlaying(players):
    res = {}
    for player in players:
        name = nameCleaner(player['first_name'] + ' ' + player['second_name'])
        res[name] = player['chance_of_playing_this_round']
    return res