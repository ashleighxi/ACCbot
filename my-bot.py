from __future__ import print_function
import discord
from datetime import date, datetime, timedelta
from operator import itemgetter
import mysql.connector
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author !=  client.user:
        if message.content.startswith('!sr'):
            parse_result = parseReport(message)
            storeScoreReport(parse_result)
            await message.channel.send('Thank you for reporting your score!')
            return
        elif message.content.startswith('!tid'):
            getTeamID(message)
            return
        elif message.content.startswith('!teams'):
            queryTeamList()
            return
        elif message.content.startswith('!standings'):
            standings_string = getStandings()
            await message.channel.send(standings_string)
            return

    else:
        return

def queryTeamList():
    cnx = mysql.connector.connect(user='', password='', database='acc_league')
    cursor = cnx.cursor()
    query = ("SELECT team_id, team_name, matches_won, matches_lost FROM teams")
    cursor.execute(query)
    for (team_id, team_name, matches_won, matches_lost) in cursor:
        print("{}({}): {}-{}".format(team_name, team_id, matches_won, matches_lost))
    cursor.close()
    cnx.close()
    return

def getTeamID(message):
    splitText = message.content.split()
    teamIDs = []
    for i in splitText:
        txt = i[1:-1]
        teamIDs.append(txt)
    print(splitText)
    print(teamIDs)
    return

def parseReport(message):
    splitText = message.content.split()
    blue_team = splitText[1][3:-1]
    orange_team = splitText[3][3:-1]
    score = splitText[2].split('-')
    blue_team_score = score[0]
    orange_team_score = score[1]
    match_data = [blue_team, orange_team, int(blue_team_score), int(orange_team_score)]
    print("parsing message:", match_data[0], match_data[2], '-', match_data[3], match_data[1])
    return match_data

def storeScoreReport(data):
    cnx = mysql.connector.connect(user='', password='', database='acc_league')
    cursor = cnx.cursor()
    today = datetime.now().date()
    winner = ''
    loser = ''

    if data[2] > data[3]:
        winner = data[0]
        loser = data[1]
    else:
        winner = data[1]
        loser = data[0]

    add_match = ("INSERT INTO matches "
                   "(match_date, blue_team_id, orange_team_id, blue_team_score, orange_team_score, winner_id) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")
    match_data = [today, data[0], data[1], data[2], data[3], winner]

    cursor.execute(add_match, match_data)
    #update record in teams table
    wins = 0
    losses = 0
    winner_query = ("SELECT matches_won FROM teams WHERE team_id = %s")
    loser_query = ("SELECT matches_lost FROM teams WHERE team_id = %s")
    cursor.execute(winner_query, (winner,))
    winner_result = cursor.fetchone()
    while winner_result is not None:
        wins = winner_result[0] + 1
        winner_result = cursor.fetchone()
    cursor.execute(loser_query, (loser,))
    loser_result = cursor.fetchone()
    while loser_result is not None:
        losses = loser_result[0] + 1
        loser_result = cursor.fetchone()
    winner_update = ("UPDATE teams SET matches_won = %s WHERE team_id = %s")
    loser_update = ("UPDATE teams SET matches_lost = %s WHERE team_id = %s")
    updates = [
    (wins, winner),
    (losses, loser)
    ]
    cursor.execute(winner_update, updates[0])
    cursor.execute(loser_update, updates[1])
    cnx.commit()
    cursor.close()
    cnx.close()

    return

def getStandings():
    cnx = mysql.connector.connect(user='', password='', database='acc_league')
    cursor = cnx.cursor()
    league_query = ("SELECT team_name, matches_won, matches_lost, division, games_won, games_lost FROM teams ORDER BY matches_won DESC")
    cursor.execute(league_query)
    standings_list = []
    a_standings = []
    c_standings = []
    overall = ''
    atlantic = ''
    coastal = ''
    for (team_name, matches_won, matches_lost, division, games_won, games_lost) in cursor:
        win_perc = Float((games_won + game_lost)) / Float(games_won)
        print(win_perc)
        standings_list.append((team_name, matches_won, matches_lost, games_won, games_lost, win_perc))
        if division == 'Atlantic':
            a_standings.append((team_name, matches_won, matches_lost, games_won, games_lost, win_perc))
        else:
            c_standings.append((team_name, matches_won, matches_lost, games_won, games_lost, win_perc))
    standings_list.sort(key = itemgetter(5))
    a_standings.sort(key = itemgetter(5))
    c_standings.sort(key = itemgetter(5))
    for team in standings_list:
        s = "{}. {} ({}-{})\n".format(standings_list.index(team) + 1, team[0], team[1], team[2])
        overall += s
    for team in a_standings:
        s = "{}. {} ({}-{})\n".format(a_standings.index(team) + 1, team[0], team[1], team[2])
        atlantic += s
    for team in c_standings:
        s = "{}. {} ({}-{})\n".format(c_standings.index(team) + 1, team[0], team[1], team[2])
        coastal += s

    overall_header = '__**Overall**__\n'
    a_header = '__**Atlantic**__\n'
    c_header = '__**Coastal**__\n'
    sep = '\n\n'
    final_string = overall_header + overall + sep + a_header + atlantic + sep + c_header + coastal
    cursor.close()
    cnx.close()
    return final_string







client.run('')
