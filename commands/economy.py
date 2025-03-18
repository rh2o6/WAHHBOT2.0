import discord
from discord.ext import commands
from discord import app_commands
import random
import datafunctions
import content
import time
from  modals.bankmodals import *

def setup(client):
    @client.tree.command()
    async def balance(interaction: discord.Interaction):
        useridentify = interaction.user.id
        datafunctions.userdbcheck(useridentify)
        balance = datafunctions.checkcoins(useridentify)
        bankbalance = datafunctions.checkbankbal(useridentify)
        banklvl = datafunctions.checkbanklvl(useridentify)

        async def refresh_callback(interaction):
            # Assuming this inner function can access 'useridentify' directly
            # Recalculate the balance in case it has changed

            if interaction.user.id == useridentify:
                new_balance = datafunctions.checkcoins(useridentify)
                newbankbal = datafunctions.checkbankbal(useridentify)
                new_embed = discord.Embed(title=f"{content.coinemoji}{interaction.user} Currency:", description=f"**Coins**:\n{content.coinemoji}{str(new_balance)} \n **Bank Balance**: \n{newbankbal}/{content.maxbankbalance[banklvl]}\n**Bank Level**:{banklvl}", color=0x4dff4d)
                # Acknowledge the interaction by editing the message with the new embed
                await interaction.response.edit_message(embed=new_embed, view=view)
            else:
                await interaction.response.send_message("Not for you!",ephemeral=True)


        async def deposit_callback(interaction):
            if interaction.user.id == useridentify:
                await interaction.response.send_modal(depositModal())
            else:
                await interaction.response.send_message("Not for you!",ephemeral=True)
        
        async def withdraw_callback(interaction):
            if interaction.user.id == useridentify:
                await interaction.response.send_modal(withdrawModal())
            else:
                await interaction.response.send_message("Not for you!",ephemeral=True)
                
        

        # Button creation with the callback function
        refreshbutton = discord.ui.Button(style=discord.ButtonStyle.primary, label="Refresh", custom_id="check_balance")
        refreshbutton.callback = refresh_callback  # Assign the callback

        depositbutton = discord.ui.Button(style=discord.ButtonStyle.blurple,label="Deposit")
        depositbutton.callback = deposit_callback

        withdrawbutton = discord.ui.Button(style=discord.ButtonStyle.blurple,label="Withdraw")
        withdrawbutton.callback = withdraw_callback


        bankembed = discord.Embed(title=f"{content.coinemoji}{interaction.user} Currency:", description=f"**Coins**:\n{content.coinemoji}{str(balance)} \n **Bank Balance**: \n{bankbalance}/{content.maxbankbalance[banklvl]}\n **Bank Level**: {banklvl}", color=0x4dff4d)
        view = discord.ui.View()
        view.add_item(refreshbutton)
        view.add_item(depositbutton)
        view.add_item(withdrawbutton)
        await interaction.response.send_message(embed=bankembed, view=view)






        
    @client.tree.command()
    @app_commands.describe(recipient = "Enter person you want to transfer coins to",transferamount = "Enter amount to transfer")
    async def transfer(interaction:discord.Interaction, recipient: discord.Member,transferamount:int):
        sender = interaction
        datafunctions.userdbcheck(sender.user.id)
        datafunctions.userdbcheck(recipient.id)
        sender_balance = datafunctions.checkcoins(sender.user.id)
        recipient_balance = datafunctions.checkcoins(recipient.id)
        mystr = ''
        
        if transferamount <= 0:
            mystr ='Please enter a valid amount of coins to transfer'
            fail_embed = discord.Embed(title="Transfer Failed", description=mystr)
            fail_embed.set_image(url='https://i.redd.it/9bpmrcwpa7ra1.jpg')
            await interaction.response.send_message(embed=fail_embed)
            return

        if sender_balance < transferamount:
            mystr = "Transfer has failed since you don't have enough money to transfer the requested amount."
            fail_embed = discord.Embed(title="Transfer Failed", description=mystr)
            fail_embed.set_image(url='https://i.redd.it/9bpmrcwpa7ra1.jpg')
            await interaction.response.send_message(embed=fail_embed)
        else:
            sender_balance -= transferamount
            recipient_balance += transferamount
            datafunctions.updatecoins(sender_balance, sender.user.id)
            datafunctions.updatecoins(recipient_balance, recipient.id)
            transfer_embed = discord.Embed(title="Transfer Success!", description=f"You have transferred {content.coinemoji} {transferamount} to {recipient.mention}!")
            await interaction.response.send_message(embed=transfer_embed)
        

        useridentify = interaction.user.id
        currentbal = datafunctions.checkbankbal(useridentify)
        banklvl = datafunctions.checkbanklvl(useridentify)
        usercoins = datafunctions.checkcoins(useridentify)
        newbal = currentbal - withdrawamt
        if newbal < 0:
            await interaction.repsonse.send_message("Withdraw failed, insufficient balance to withdraw amount")
        else:
            datafunctions.updatebank(newbal,useridentify)
            usercoins += withdrawamt
            datafunctions.updatecoins(usercoins,useridentify)
            
            await interaction.response.send_message("Withdrawl Successful")




    @client.tree.command(name="work")
    async def work(interaction:discord.Interaction):
        useridentify = interaction.user.id
        datafunctions.userdbcheck(useridentify)
        existingcoins = datafunctions.checkcoins(useridentify)
        jobselect = random.choice(content.workoptions)
        earnings = random.randint(20,50)
        if useridentify in content.workcooldowns:
            time_passed = time.time() - content.workcooldowns[useridentify]
            if time_passed < content.WORKCD:
                # Calculate remaining time
                remaining_time = content.WORKCD - time_passed
                # Format remaining time into minutes and seconds
                minutes, seconds = divmod(int(remaining_time), 60)
                await interaction.response.send_message(f"You're on cooldown. Please wait {minutes} minutes and {seconds} seconds before working again.")
                return
            else:
                # If cooldown is over, delete the user from cooldowns
                del content.workcooldowns[useridentify]
        workstr = f"You made <a:Coin:1224446854708727908>{earnings}"
        workembed = discord.Embed(title="Off to work!",description=workstr,color =0x4dff4d)
        workembed.set_footer(text=f"Worked a shift as a {jobselect}")
        await interaction.response.send_message(embed=workembed)
        datafunctions.updatecoins(earnings+existingcoins, useridentify)
        currentshifts = datafunctions.checktotalshifts(useridentify)
        if currentshifts == None:
            currentshifts = 0
        currentshifts += 1
        
        datafunctions.workadjust(currentshifts,useridentify)
        content.workcooldowns[useridentify] = time.time()