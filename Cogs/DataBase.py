from asyncio.windows_events import NULL
import pymongo
from pymongo import MongoClient
import discord
from discord.ext import commands
from discord import Member
import random
import asyncio
from discord.ext.commands import has_permissions, MissingPermissions

#mongodb connection string
cluster = MongoClient("")
#cluster name
db = cluster['DicordBot']
#collection name
collection = db['UserData']



class DataBase(commands.Cog):
    def __init__(self, client):
        self.client = client

           
    @commands.command(name='tempmute')
    @has_permissions(manage_roles=True ,ban_members=True)
    async def _tempmute(self, ctx, member: discord.Member, time: int, d, *, reason=None):
        """Temporarily mute a member"""
        guild = ctx.guild

        for role in guild.roles:
            if role.name == "Muted":
                await member.add_roles(role)
                #inserts muted members ID into DB
                post = {"_id": member.id, "name": member.nick, "time": time, "format": d, "reason": reason}
                collection.insert_one(post)

                embed = discord.Embed(title="Muted", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.light_gray())
                embed.add_field(name="Reason:", value=reason, inline=False)
                embed.add_field(name="Time left for the mute:", value=f"{time}{d}", inline=False)
                await ctx.send(embed=embed)

                if d == "s":
                    await asyncio.sleep(time)

                if d == "m":
                    await asyncio.sleep(time*60)

                if d == "h":
                    await asyncio.sleep(time*60*60)

                if d == "d":
                    await asyncio.sleep(time*60*60*24)

                await member.remove_roles(role)
                collection.delete_one(post)

                embed = discord.Embed(title="Unmute (temp) ", description=f"Unmuted -{member.mention} ", colour=discord.Colour.light_gray())
                await ctx.send(embed=embed)
    @_tempmute.error
    async def tempmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.channel.send("Sorry , you do not have permissions to do that!")

    @commands.command(name='mutedlist')
    @has_permissions(manage_roles=True ,ban_members=True)
    async def _mutedlist(self, ctx):
        """Shows muted player list"""
        if collection.count() == 0:
            await ctx.channel.send("No one is muted")
        for x in collection.find():
            await ctx.channel.send(x)
    @_mutedlist.error
    async def mutedlist_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.channel.send("Sorry , you do not have permissions to do that!")
    
                
   

def setup(client):
    client.add_cog(DataBase(client))
