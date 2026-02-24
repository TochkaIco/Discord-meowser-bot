import discord
from discord import app_commands
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

# --- Setup and Config ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

trigger_messages = ["cat", "car", "kitty", "furry", "furries"]

# Direct .gif links are required for embeds to display them properly
gif_bites = [
    "https://c.tenor.com/Yk5VLCkqfwYAAAAd/tenor.gif",
    "https://c.tenor.com/J-d8KHJfE9kAAAAd/tenor.gif",
    "https://c.tenor.com/4nSJ7HPC6rQAAAAd/tenor.gif",
]

def random_meow():
    meow_list = [
        "meow-mror-mrppppp :333333",
        "meow~",
        "-# mwow~",
        "meowieeeeeeeeeeeee :>",
        "mreowiehehe >:3",
        "nom ^.^",
        "*Suddenly feel like biting*",
        "Did somebody say my name? >:3",
        "Imma bite the <@&1413982969093161070> :<",
        "We live in a twilight world...and?",
        "I have been summoned!",
    ]
    return random.choice(meow_list)

def random_gif():
    return random.choice(gif_bites)

# --- Bot Initialization ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# --- Events ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check for keywords and meow once per message
    msg_lower = message.content.lower()
    for unit in trigger_messages:
        if unit in msg_lower:
            await message.channel.send(random_meow())
            break 

    await bot.process_commands(message)

# --- Slash Commands ---
@bot.tree.command(name="bite", description="Bite someone!")
@app_commands.describe(target="The user you want to chomp")
async def bite(interaction: discord.Interaction, target: discord.User):
    # 1. Immediate check: If user bites themselves, send ephemeral message and stop.
    if target == interaction.user:
        return await interaction.response.send_message(
            "You can’t bite yourself! 🫢", 
            ephemeral=True
        )

    # 2. Defer immediately: This tells Discord to wait up to 15 mins.
    # This prevents the "Unknown Interaction" 404 error.
    await interaction.response.defer()

    try:
        responses = [
            f"{interaction.user.mention} bites {target.mention}",
            f"{interaction.user.mention} chomps on {target.mention}",
        ]

        embed = discord.Embed(
            description=random.choice(responses), 
            color=discord.Color.red()
        )
        embed.set_image(url=random_gif())

        # 3. Use followup.send because we already deferred the response.
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        print(f"Error in bite command: {e}")
        # If something fails, let the user know since we already deferred
        await interaction.followup.send("Something went wrong while trying to bite!", ephemeral=True)

# --- Run ---
bot.run(TOKEN)
