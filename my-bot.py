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
        if message.content.startswith('$hello'):
            print('they said hello')
            await message.channel.send('Hello!')
    else:
        return



client.run('NjgwMTI4NTUwMTMyNTE0ODI2.Xk7ZKg.YpUL9LSoZ1X-syrVqyFk8h3FYxI')
