import discord
import datafunctions
import content












class depositModal(discord.ui.Modal,title="Bank Deposit"):
    depositamount = discord.ui.TextInput(label="Enter amount to deposit",placeholder="Enter money here",style=discord.TextStyle.short)

    async def on_submit(self,interaction:discord.Interaction):
        if not(self.depositamount.value.isnumeric()):
            await interaction.response.send_message("Invalid Amount, Please enter a valid amount")
        depositamt = int(self.depositamount.value)
        useridentify = interaction.user.id
        usercoins = datafunctions.checkcoins(useridentify)
        currentbal = datafunctions.checkbankbal(useridentify)
        banklvl = datafunctions.checkbanklvl(useridentify)
        newbal = currentbal + depositamt
        if newbal > content.maxbankbalance[banklvl]:
            await interaction.response.send_message("Deposit will exceed bank capacity, try again with a lower amount")
        elif depositamt > usercoins:
            await interaction.response.send_message("Deposit failed, not enough coins to depoist that amount")

        elif depositamt < 0:
            await interaction.response.send_message("Invalid Amount, Please enter a valid amount")

        else:
            newcoinsval = usercoins - depositamt
            datafunctions.updatecoins(newcoinsval,useridentify)
            datafunctions.updatebank(newbal,useridentify)

            await interaction.response.send_message("Deposit Successful")


class withdrawModal(discord.ui.Modal,title="Bank Withdraw"):
    withdrawamt = discord.ui.TextInput(label="Enter amount to withdraw",placeholder="Enter money here",style=discord.TextStyle.short)

    async def on_submit(self,interaction:discord.Interaction):
        useridentify = interaction.user.id

        if not(self.withdrawamt.value.isnumeric()):
            await interaction.response.send_message("Invalid Amount, Please enter a valid amount")


        withdrawamt = int(self.withdrawamt.value)
        currentbal = datafunctions.checkbankbal(useridentify)
        banklvl = datafunctions.checkbanklvl(useridentify)
        usercoins = datafunctions.checkcoins(useridentify)
        newbal = currentbal - withdrawamt
        if newbal < 0:
            await interaction.response.send_message("Withdraw failed, insufficient balance to withdraw amount")
        
        elif withdrawamt < 0:
            await interaction.response.send_message("Invalid Amount, Please enter a valid amount")

        else:
            datafunctions.updatebank(newbal,useridentify)
            usercoins += withdrawamt
            datafunctions.updatecoins(usercoins,useridentify)
        
            await interaction.response.send_message("Withdrawl Successful")