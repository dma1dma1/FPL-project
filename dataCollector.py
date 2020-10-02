import requests
import re
import json
from bs4 import BeautifulSoup

GENERIC_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
FIXTURE_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
PLAYER_URL = 'https://fantasy.premierleague.com/api/element-summary/'

def getGenericFPLData(url = GENERIC_URL):
    '''
    Gets all generic FPL information

    Param:
        url (str): URL of generic FPL API

    Return:
        deadlines (list): list of all gameweek deadlines for transferring players
        teams (list): list of lists containing team id and team name
        players (list): list of lists containing player information
    '''
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Generic data error code:" + str(r.status_code))
    json = r.json()

    deadlines = [event['deadline_time'] for event in json['events']]
    teams = [[team['id'], team['name']] for team in json['teams']]
    players = json['elements']
    return deadlines, teams, players

def getFixtureFPLData(url = FIXTURE_URL):
    '''
    Gets fixture data

    Param:
        url (str): URL of fixture FPL API

    Return:
        information in JSON format
    '''
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Fixture data error code:" + str(r.status_code))
    json = r.json()
    return json

def getPlayerFPLData(id, url = PLAYER_URL):
    '''
    Gets FPL player data

    Param:
        id (int): id of player requested
        url (str): URL of generic FPL API

    Return:
        information in JSON format
    '''
    r = requests.get(url + str(id) + '/')
    if r.status_code != 200:
        raise Exception("Player data error code:" + str(r.status_code))
    json = r.json()
    return json

def getFBrefdata(url):
    '''
    Uses bs4 to scrape data from any fbref.com squad and player stats page

    Param:
        url (str): url of page to be scraped

    Return:
        team_table (list): list of dicts containing team information
        player_table (list): list of dicts containing player information
    '''
    r = requests.get(url)

    # Regex to remove comments needed for parser to parse correctly
    comments = re.compile("<!--|-->")
    html = BeautifulSoup(comments.sub("", r.text), 'html.parser')

    # Body and Head processed separately since there are 2 theads per table
    tableheads = [thead.find_all(class_ = False) for thead in html.find_all('thead')]
    team_head = tableheads[0][0].text.strip().split('\n')
    player_head = tableheads[1][1].text.strip().split('\n')

    # Table body processing
    bodies = html.find_all('tbody')
    team_data = [[data.text for data in tr] for tr in bodies[0].find_all('tr')]
    player_data = [[data.text for data in tr] for tr in bodies[1].find_all('tr', class_ = False)]
    
    # Combine head and body into json
    team_table = [dict(zip(team_head, data)) for data in team_data]
    player_table = [dict(zip(player_head, data)) for data in player_data]

    return team_table, player_table

print(getGenericFPLData())