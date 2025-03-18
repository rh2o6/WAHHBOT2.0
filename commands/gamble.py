import discord
from discord.ext import commands
from discord import app_commands
import random
import datafunctions
import content
import time

def setup(client):
    @client.tree.command()
    @app_commands.describe(betamt = "Enter amount to gamble")
    async def gamble(interaction:discord.Interaction,betamt:int):
        useridentify = interaction.user.id
        datafunctions.userdbcheck(useridentify)
        data = datafunctions.checkcoins(useridentify)
        

        if betamt < 0:
            await interaction.response.send_message("Invalid bet amount")

        elif  data < betamt:
            await interaction.response.send_message("To poor to gamble")
            return


        if useridentify in gamblecooldowns:
            time_passed = time.time() - gamblecooldowns[useridentify]
            if time_passed < content.GAMBLECD:
                # Calculate remaining time
                remaining_time = content.GAMBLECD - time_passed
                # Format remaining time into minutes and seconds
                minutes, seconds = divmod(int(remaining_time), 60)
                await interaction.response.send_message(f"You're on cooldown. Please wait {minutes} minutes and {seconds} seconds before attempting to gamble again.")
                return
            else:
                # If cooldown is over, delete the user from cooldowns
                del gamblecooldowns[useridentify]



        roll = random.randint(1,2)
        dictbool = {True:"Won",False:"Lost"}
        if roll == 1:
            status = False
        else:
            status = True

        if status == True:
            final = data + betamt*2
            mystr = f"You Won {content.coinemoji}{betamt*2}"
        else:
            status == False
            final = data - betamt
            mystr = f"You Lost {content.coinemoji}{betamt}"
        
        embed = discord.Embed(title="Rolling...",description=f'{mystr}',color=0x4dff4d)
        embed.set_footer(text="Did you know that 99%, of gamblers give up before a jackpot!")
        embed.set_image(url = "https://static.wikia.nocookie.net/siivagunner/images/e/e0/Waluigi-Pinball.png/revision/latest?cb=20200515232537")
        datafunctions.updatecoins(final,useridentify)
        gamblecooldowns[useridentify] = time.time()
        await interaction.response.send_message(embed=embed)

