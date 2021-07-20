import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('{0.user} online! Ready to begin operations!'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(os.environ['TOKEN'])
