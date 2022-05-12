import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import random
import youtube_dl
import asyncio
import pymongo
from pymongo import MongoClient
import logging
import os

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


client = commands.Bot(command_prefix='.', owner_id=127753524623704064)


#cogs
@client.command()
async def load (ctx, extension):
    client.load_extension(f'Cogs.{extension}')
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')
        

#commands
@client.command(name='description')
async def description(context):
    """Bots description"""

    descEmbed = discord.Embed(title="Description", description="Python bot test", color=0x0000ff)
    descEmbed.add_field(name="Version code:", value="v1.0.0",inline=False)
    descEmbed.add_field(name="Date released:", value="2021-05-08",inline=False)
    descEmbed.set_author(name="Tomas J")

    await context.message.channel.send(embed=descEmbed)


#kick
@client.command(name='kick', pass_context=True)
@has_permissions(ban_members=True)
async def _kick(ctx, member : discord.Member, *,reason=None):
    """Kick member"""
    await member.kick(reason=reason)
@_kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send("Sorry , you do not have permissions to do that!")

#ban
@client.command(name='ban', pass_context=True)
@has_permissions(manage_roles=True, ban_members=True)
async def _ban(ctx, member : discord.Member, *,reason=None):
    """Bans member"""
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself")
        return
    if reason==None:
        reason = "No reason"
    message = f"You have been banned from {ctx.guild.name} for {reason}"
    await member.send(message)
    await member.ban(reason=reason)
    await ctx.channel.send(f"{member} is banned")
@_ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send("Sorry , you do not have permissions to do that!")


#unban
@client.command(name='unban', pass_context=True)
@has_permissions(manage_roles=True, ban_members=True)
async def _unban(ctx, *,member):
    """Unbans member"""
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.send(f"Unbanned {user.name}#{user.discriminator}")
@_unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send("Sorry , you do not have permissions to do that!")

#mute
@client.command(name='mute', pass_context=True)
@has_permissions(manage_roles=True)
async def _mute (ctx, member : discord.Member):
    """Mutes member in all channels"""
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
    for channel in guild.channels:
        await channel.set_permissions(mutedRole, speak=False, send_messages=False)
    await member.add_roles(mutedRole)
    await ctx.channel.send(f"{member} has been muted")
@_mute.error
async def mute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send("Sorry , you do not have permissions to do that!")

#unmute
@client.command(name='unmute', pass_context=True)
@has_permissions(manage_roles=True)
async def _unmute (ctx, member: discord.Member):
    """Unmutes member"""
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await member.send(f" you have unmutedd from: - {ctx.guild.name}")
    await ctx.channel.send(f"{member} has been unmuted")
@_unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send("Sorry , you do not have permissions to do that!")

@client.event
async def on_message(message):
    badwords = ["test123", "badword", "dainauskas"]

    if message.content.lower() in badwords:
        await message.delete()

    await client.process_commands(message)




@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    bottest_channel = client.get_channel(838729652646314014)
    await bottest_channel.send('Im alive')




#bot token
client.run('ODM4NzI4ODI5ODc5MDU4NDUz.YI_VFw.YFibeOFFR8n-nGrQB8wI59bEoRk')