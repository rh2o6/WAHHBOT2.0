import discord
from discord.ext import commands
from discord import app_commands
import random
import datafunctions
import content
import time
def setup(client):
    @client.tree.command()
    async def fish(interaction: discord.Interaction):
        useridentify = interaction.user.id
        catchornot = random.randint(1, 2)
        rodtype = datafunctions.checkrod(useridentify)

        if catchornot == 1:
            failembed = discord.Embed(title="Caught Nothing", description="Unlucky, Nothing bit...")
            await interaction.response.send_message(embed=failembed)
        else:
            fishtier = content.fish_roll(content.fish_data["chances"])
            fishcaught = random.choice(content.fish_data["categories"][fishtier])

            # quant = datafunctions.checkfishamt(useridentify, fishcaught)
            # quant += 1
            # datafunctions.updatefishbucket(useridentify, fishcaught, quant)

            fish_emoji = content.fish_data["emojis"].get(fishcaught, "")
            fish_name = content.fish_data["proper_names"].get(fishcaught, fishcaught)

            await interaction.response.send_message(
                f"Congrats! You caught a {fish_emoji} {fish_name} of {fishtier} rarity with your {rodtype}!"
            )

            datafunctions.updatefishbucket(useridentify, fishcaught, 1)


    @client.tree.command()
    async def checkbucket(interaction: discord.Interaction):
        useridentify = interaction.user.id
        fish_bucket = datafunctions.getfishbucket(useridentify)

        if not fish_bucket:
            # If the bucket is empty or doesn't exist
            empty_embed = discord.Embed(
                title="Your Fish Bucket",
                description="Your bucket is empty! Go fishing to catch some fish!",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=empty_embed)
        else:
            # Create an embed to display the fish bucket
            bucket_embed = discord.Embed(
                title="Your Fish Bucket",
                description="Here are the fish you've caught:",
                color=discord.Color.green()
            )

            for fish, quantity in fish_bucket.items():
                fish_emoji = content.fish_data["emojis"].get(fish, "")
                fish_name = content.fish_data["proper_names"].get(fish, fish)
                bucket_embed.add_field(
                    name=f"{fish_emoji} {fish_name}",
                    value=f"Quantity: {quantity}",
                    inline=False
                )

            await interaction.response.send_message(embed=bucket_embed)

