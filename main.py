import discord
from discord.ext import commands
import os
import random
import requests
import asyncio
from dotenv import load_dotenv
import sys

if os.path.exists("bot.lock"):
    print("CRITICAL: Another instance is already running. Delete 'bot.lock' if this is an error.")
    sys.exit(1)
with open("bot.lock", "w") as f:
    f.write(str(os.getpid()))

try:
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    TEACHGPT_API_KEY = os.getenv("TEACHGPT_API_KEY")

    processed_messages = set()
    trigger_messages = ["cat", "car", "kitty", "furry", "furries"]

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

    message_lock = asyncio.Lock()


    def random_meow():
        meow_list = ["meow~", "mreowiehehe >:3", "nom ^.^", "*Suddenly feel like biting*"]
        return random.choice(meow_list)


    def get_teachgpt_response():
        url = "https://teachgpt-teachgpt-test.apps.okd.ssis.nu/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {TEACHGPT_API_KEY}", "Content-Type": "application/json"}
        topics = ["Kubernetes internals", "Git commands", "Architecture in system design", "Advantages/Disadvantages of Laravel", "Docker commands", "Docker networking", "vim vs neovim vs vis, what's your pick?", "Linux kernel", "Cat facts"]
        selected_topic = random.choice(topics)
        data = {
            "model": "Meta-Llama-3.3-70B-Instruct-AWQ",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a quirky cat. Provide a very obscure, advanced, or surprising fact about {selected_topic}. Avoid common knowledge. Be concise."
                },
                {
                    "role": "user",
                    "content": "Meow! Give me a secret dev tip!"
                }
            ],
            "temperature": 0.9,
            "frequency_penalty": 1.2,
            "presence_penalty": 0.5
        }
        try:
            r = requests.post(url, headers=headers, json=data, timeout=5)
            return r.json()["choices"][0]["message"]["content"]
        except:
            return None


    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        # Force synchronous command processing
        await bot.process_commands(message)

        # Use lock to ensure only one trigger logic block runs at once
        async with message_lock:
            if message.id in processed_messages:
                return

            if message.content.startswith('!'):
                return

            if any(unit in message.content.lower() for unit in trigger_messages):
                processed_messages.add(message.id)

                # Logic execution
                if random.random() < 0.5:
                    resp = await asyncio.to_thread(get_teachgpt_response)
                    await message.reply(resp if resp else random_meow())
                else:
                    await message.reply(random_meow())


    bot.run(TOKEN)

finally:
    # Cleanup lock file on exit
    if os.path.exists("bot.lock"):
        os.remove("bot.lock")