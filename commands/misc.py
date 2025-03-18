import discord
from discord.ext import commands
from discord import app_commands
import random
import datafunctions
import content
import time

def setup(client):
    @client.tree.command()
    async def register(interaction: discord.Interaction):
        useridentify = interaction.user.id
        regembed = ""

        if not(datafunctions.userexists):


            datafunctions.userdbcheck(useridentify)
      
            regembed = discord.Embed(title="New User Registration",description = "Congrats! You are now Registerd",color=content.purple)
            regembed.set_image(url='https://www.kotaku.com.au/wp-content/uploads/2018/06/15/umkr4qwixrkw7txyv40m.jpg?quality=75&w=640&h=360&crop=1')

        else:

            regembed =discord.Embed(title="New User Registration",description = "You are already registered!",color=content.purple)
        await interaction.response.send_message(embed=regembed)