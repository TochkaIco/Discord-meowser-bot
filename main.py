import discord
from discord import app_commands
from discord.ext import commands
import os
import random
import requests
import asyncio
from dotenv import load_dotenv

# --- Setup and Config ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
TEACHGPT_API_KEY = os.getenv("TEACHGPT_API_KEY")

trigger_messages = ["cat", "car", "kitty", "furry", "furries"]

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


def get_teachgpt_response():
    url = "https://teachgpt-teachgpt-test.apps.okd.ssis.nu/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TEACHGPT_API_KEY}"
    }

    data = {
        "model": "Meta-Llama-3.3-70B-Instruct-AWQ",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a chaotic discord bot assistant. Flip a coin mentally. "
                    "50% of the time, respond entirely as a cute/chaotic cat using lots of meows, purrs, and emojis. "
                    "The other 50% of the time, tell a random, genuinely interesting or niche fact about Kubernetes (k8s). "
                    "Keep your response concise, under 3 short sentences."
                )
            },
            {
                "role": "user",
                "content": "Someone triggered you! Give your random cat response or k8s fact now."
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API Error: {e}")
        return None


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
    # Prevent the bot from replying to its own messages
    if message.author == bot.user:
        return

    msg_lower = message.content.lower()
    for unit in trigger_messages:
        if unit in msg_lower:
            # 50% chance to fetch from TeachGPT API
            if random.random() < 0.5:
                # Triggers the native visual "Bot is typing..." feedback
                async with message.channel.typing():
                    # Runs the blocking request code off the main loop to keep bot fast
                    api_response = await asyncio.to_thread(get_teachgpt_response)

                if api_response:
                    await message.reply(api_response)
                else:
                    # Fallback to local meows if API errors out
                    await message.reply(random_meow())
            else:
                # The remaining 50% of the time, pull directly from the local list
                await message.reply(random_meow())
            break

    await bot.process_commands(message)


# --- Slash Commands ---
@bot.tree.command(name="bite", description="Bite someone!")
@app_commands.describe(target="The user you want to chomp")
async def bite(interaction: discord.Interaction, target: discord.User):
    # 1. Validation check
    if target == interaction.user:
        return await interaction.response.send_message(
            "You can’t bite yourself! 🫢",
            ephemeral=True
        )

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

        await interaction.edit_original_response(embed=embed)

    except Exception as e:
        print(f"Error in bite command: {e}")
        try:
            await interaction.followup.send("Something went wrong while trying to bite!", ephemeral=True)
        except Exception:
            pass


# --- Run Bot ---
bot.run(TOKEN)