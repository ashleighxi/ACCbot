import discord
import datetime
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
            parseReport(message)
            #await message.channel.send('Thank you for reporting the score!')
        elif message.content.startswith('!tid'):
            getTeamID(message)
        elif message.content.startswith('!teams'):
            queryTeamList()

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
    teamOne = splitText[1][1:-1]
    teamTwo = splitText[3][1:-1]
    score = splitText[2]
    print("parsing message: ", teamOne, score, teamTwo)
    return


client.run('')
