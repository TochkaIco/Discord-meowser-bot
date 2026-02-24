import discord
from discord import app_commands
from discord.ext import commands
import os
import random
from random import randint
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
# arch_site = """Just go and install Arch ISO already :<
# \nhttps://archlinux.org/"""
trigger_messages = [
    "cat",
    "car",
    "kitty",
    "furry",
    "furries",
]
gif_bites = [
    "https://tenor.com/view/chomp-bite-arm-gif-7083692912057941766.gif",
    "https://tenor.com/view/mikisi-kisi-kiss-gif-27218966.gif",
    "https://tenor.com/view/slow-cat-bite-cat-bite-slow-gif-26064423.gif",
]

def random_meow():
    meow_list = [
        "meow-mror-mrppppp :333333",
        "meow~",
        "-# mwow~",
        "meowieeeeeeeeeeeee :>",
        "mreowiehehe >:3",
        "nom ^.^",
        "*Suddenly feel like biting\*",
        "Did somebody say my name? >:3",
        "Imma bite the <@&1413982969093161070> :<",
        "We live in a twilight world...and?",
        "I have been summoned!",
]
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
    for unit in trigger_messages:
        if unit in message.content.lower():
            await message.channel.send(random_meow())
    # if "arch" in message.content.lower():
    #     await message.channel.send(arch_site)
    await bot.process_commands(message)

@bot.tree.command(name="bite", description="Bite someone!")
async def bite(interaction: discord.Interaction, target: discord.User):
    # 1. Check self-bite immediately (this is fast)
    if target == interaction.user:
        return await interaction.response.send_message("You can’t bite yourself! 🫢", ephemeral=True)

    # 2. Defer the interaction. This buys you 15 minutes.
    # We use thinking=False so the "Bot is thinking..." message is cleaner.
    await interaction.response.defer()

    responses = [
        f"{interaction.user.mention} bites {target.mention}",
        f"{interaction.user.mention} chomps on {target.mention}",
    ]

    # 3. Perform your logic (even if random_gif takes 4 seconds, you're safe now)
    embed = discord.Embed(description=random.choice(responses), color=discord.Color.red())
    
    # If random_gif is an async function, remember to 'await' it!
    gif_url = random_gif() 
    embed.set_image(url=gif_url)

    # 4. Use followups to send the final message after deferring
    await interaction.followup.send(embed=embed)

bot.run(TOKEN)
