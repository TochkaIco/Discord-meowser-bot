import discord
import os
from random import randint
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

def random_meow():
    meow_list = ["meow-mror-mrppppp :333333", "meow~", "-# mwow~", "meowieeeeeeeeeeeee :>", "mreowiehehe >:3"]
    i = randint(0, len(meow_list) - 1)
    return meow_list[i]

# Intents are required for message content
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if ("cat" in message.content.lower()) or ("furry" in message.content.lower()):
        await message.channel.send("meow-mror-mrpppppp >:3")

client.run(TOKEN)
