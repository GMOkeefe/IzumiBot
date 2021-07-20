import discord
import os

import commands

client = discord.Client()

@client.event
async def on_ready():
  print('{0.user} online! Ready to begin operations!'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!hello'):
    commands.hello(message.channel)
  
  if message.content.startswith('!pop'):
    commands.pop(message.author, message.channel)

if __name__ == "__main__":
  client.run(os.environ['TOKEN'])
