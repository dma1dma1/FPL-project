import psycopg2
from config import config
from dataCollector import getGenericFPLData
from datetime import datetime
import csv

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

def csvtodicts(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def getGameweek():
    g_data = getGenericFPLData()
    deadlines = [event['deadline_time'] for event in g_data['events']]

    # Get current time
    time = datetime.utcnow()

    # Convert deadlines to datetime while comparing
    for i in range(len(deadlines)):
        if datetime.strptime(deadlines[i], '%Y-%m-%dT%H:%M:%SZ') > time:
            return i + 1

def debug_names(player_dict):
    print('Wrong FPL name or no FPL data: ')
    for player in player_dict.values():
        try:
            player['element_type']
        except:
            print(player['player_name'])
    print('')
    '''print('No FBref data: ')
    for player in player_dict.values():
        try:
            player['gls_90']
        except:
            print(player['player_name'])'''
    return

#connect('SQL/drop.sql', isfile=True)