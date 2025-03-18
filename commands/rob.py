import discord
from discord.ext import commands
from discord import app_commands
import random
import datafunctions
import content
import time


def setup(client):
    @client.tree.command()
    @app_commands.describe(robvictim="Enter rob target")
    async def rob(interaction:discord.Interaction, robvictim:discord.Member):
        datafunctions.userdbcheck(interaction.user.id)
        recep = robvictim
        recepid = recep.id
        datafunctions.userdbcheck(recepid)
        robstatus = False
        robcheck = random.randint(1,4)
        useridentify = interaction.user.id
        thiefbalance = datafunctions.checkcoins(useridentify)
        victimbalance = datafunctions.checkcoins(recepid)
        if useridentify in content.gamblecooldowns:
            time_passed = time.time() - content.gamblecooldowns[useridentify]
            if time_passed < content.GAMBLECD:
                # Calculate remaining time
                remaining_time = content.GAMBLECD - time_passed
                # Format remaining time into minutes and seconds
                minutes, seconds = divmod(int(remaining_time), 60)
                await interaction.response.send_message(f"You're on cooldown. Please wait {minutes} minutes and {seconds} seconds before attempting to rob again.")
                return
            else:
                # If cooldown is over, delete the user from cooldowns
                del content.gamblecooldowns[useridentify]

        if robcheck == 1:
            robstatus = True
        if robstatus and victimbalance > 0:
            
            robembed = discord.Embed(title = "Robbery Success!",description=f"Successfuly stole {content.coinemoji} {victimbalance//10} from {recep.mention}")
            robembed.set_image(url="https://i.ytimg.com/vi/dISuBAGxw4w/maxresdefault.jpg")
            await interaction.response.send_message(embed=robembed)
            thiefbalance += victimbalance // 10
            victimbalance -= victimbalance // 10
            datafunctions.updatecoins(thiefbalance,useridentify)
            datafunctions.updatecoins(victimbalance,recepid)
            content.gamblecooldowns[useridentify] = time.time()
        
        elif victimbalance < 0:
            robembed = discord.Embed(title="Robbery Failed",description="Victim is to poor to be robbed. They gotta get they money up not funny up")
            await interaction.response.send_message(embed=robembed)
        else:
            robembed = discord.Embed(title="Robbery Failed",description="You were to slow and they got away")
            content.gamblecooldowns[useridentify] = time.time()
            await interaction.response.send_message(embed=robembed)

        return
