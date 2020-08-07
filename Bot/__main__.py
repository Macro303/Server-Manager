#!/usr/bin/env python3
import logging
from typing import Dict, Any

import discord
from discord import MessageType, Colour, Member, Message
from discord.ext import commands
from discord.utils import escape_markdown

from Bot import CONFIG
from Logger import init_logger

LOGGER = logging.getLogger(__name__)
COGS = ['Bot.cogs.role_management', 'Bot.cogs.admin']
bot = commands.Bot(command_prefix=commands.when_mentioned_or(CONFIG['Prefix']), case_insensitive=True)


@bot.event
async def on_ready():
    LOGGER.info(f"Logged in as: {bot.user}")
    bot.remove_command('help')
    for cog in COGS:
        bot.load_extension(cog)
    await bot.change_presence(activity=discord.Game(name='with Server details'))


@bot.event
async def on_message_delete(message: Message):
    LOGGER.info(f"Message was Deleted: {message}")
    channel = bot.get_channel(CONFIG['Channels']['Logs'])
    if channel and message.type == MessageType.default:
        embed = discord.Embed(title=f"Message Deleted *({message.id})*", color=Colour.dark_red())
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.add_field(name="Content", value=f"```{escape_markdown(message.content)}```")
        await channel.send(embed=embed)


@bot.event
async def on_message_edit(before: Message, after: Message):
    if before.author.bot or after.author.bot:
        return
    LOGGER.info(f"Message updated:\n{before}\n{after}")
    channel = bot.get_channel(CONFIG['Channels']['Logs'])
    if channel and before.type == MessageType.default and after.type == MessageType.default:
        embed = discord.Embed(title=f"Message Edited *({before.id or after.id})*", color=Colour.dark_teal())
        embed.set_author(name=before.author.name or after.author.name,
                         icon_url=before.author.avatar_url or after.author.avatar_url)
        embed.add_field(name="Old Message", value=f"```{escape_markdown(before.content)}```")
        embed.add_field(name="New Message", value=f"```{escape_markdown(after.content)}```")
        await channel.send(embed=embed)


@bot.event
async def on_member_join(member: Member):
    if member.bot:
        return
    LOGGER.info(f"New Member joined: {member}")
    channel = bot.get_channel(CONFIG['Channels']['Logs'])
    if channel:
        await channel.send(f"{member} Joined!")


@bot.event
async def on_member_remove(member: Member):
    if member.bot:
        return
    LOGGER.info(f"New Member left: {member}")
    channel = bot.get_channel(CONFIG['Channels']['Logs'])
    if channel:
        await channel.send(f"{member} left!")


def member_dict(member: Member) -> Dict[str, Any]:
    return {
        'nickname': member.nick,
        'username': member.name,
        'roles': [x.name for x in member.roles]
    }


@bot.event
async def on_member_update(before: Member, after: Member):
    if before.bot or after.bot:
        return
    if member_dict(before) == member_dict(after):
        return
    LOGGER.info(f"Member updated:\n{member_dict(before)}\n{member_dict(after)}")
    channel = bot.get_channel(CONFIG['Channels']['Logs'])
    if channel:
        embed = discord.Embed(title=f"Member Updated", color=Colour.dark_teal())
        embed.set_author(name=before.name or after.name, icon_url=before.avatar_url or after.avatar_url)
        embed.add_field(name="Old Member", value=f"```{member_dict(before)}```")
        embed.add_field(name="New Member", value=f"```{member_dict(after)}```")
        await channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)


if __name__ == "__main__":
    init_logger('Bot')
    bot.run(CONFIG['Token'], bot=True, reconnect=True)
