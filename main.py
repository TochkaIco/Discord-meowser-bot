import discord
from discord import app_commands
from discord.ext import commands
import os
import random
from random import randint
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
arch_site = """Just go and install Arch ISO already :<
\nhttps://archlinux.org/"""
gif_bites = [
    "https://tenor.com/view/chomp-bite-arm-gif-7083692912057941766",
    "https://tenor.com/view/mikisi-kisi-kiss-gif-27218966",
    "https://tenor.com/view/slow-cat-bite-cat-bite-slow-gif-26064423",
]

def random_meow():
    meow_list = ["meow-mror-mrppppp :333333", "meow~", "-# mwow~", "meowieeeeeeeeeeeee :>", "mreowiehehe >:3"]
    return random.choice(meow_list)
def random_gif():
    return random.choice(gif_bites)

# Intents are required for message content
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if ("cat" in message.content.lower()) or ("furry" in message.content.lower()):
        await message.channel.send(random_meow())
    if "arch" in message.content.lower():
        await message.channel.send(arch_site)
    await bot.process_commands(message)

@bot.tree.command(name="bite", description="Bite someone!")
async def bite(interaction: discord.Interaction, target: discord.User):
    responses = [
        f"{interaction.user.mention} bites {target.mention}",
        f"{interaction.user.mention} chomps on {target.mention}",
    ]
    if target == interaction.user:
        await interaction.response.send_message("You can’t bite yourself! 🫢", ephemeral=True)
        return
    embed = discord.Embed(description=random.choice(responses), color=discord.Color.red())
    embed.set_image(url=random_gif())
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)