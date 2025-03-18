#Discord API
import discord
from discord.ext import commands
#File Imports
import os
import importlib
import datafunctions



TOKEN = os.environ.get("bottoken") #String for Bot Token
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!",intents=intents)



# Initiate Bot stuff
@client.event
async def on_ready():
    print("Bots ready")
    synced = await client.tree.sync()
    print (f"Synced {len(synced)} commands")


def load_commands():
    command_files = ['commands.economy', 'commands.fish', 'commands.gamble', 'commands.misc', 'commands.rob']  # Include folder names
    for command_file in command_files:
        try:
            module = importlib.import_module(command_file)
            module.setup(client)
            print(f"Loaded {command_file} commands successfully.")
        except Exception as e:
            print(f"Error loading {command_file} commands: {e}")


load_commands()
datafunctions.create_or_update_fishbucket_table()
client.run(TOKEN)