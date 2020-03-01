import discord
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
        await message.channel.send(message.content)
        parseReport(message)
        await message.channel.send('Thank you for reporting the score!')
    else:
        return


def parseReport(message):
    splitText = message.content.split()
    teamOne = splitText[1]#[1:]
    teamTwo = splitText[3]#[1:]
    score = splitText[2]
    print("parsing message: ", teamOne, score, teamTwo)
    return


client.run('')
