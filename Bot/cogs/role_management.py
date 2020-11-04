#!/usr/bin/env python3
import logging
from typing import Optional

from discord.abc import GuildChannel
from discord.ext import commands
from discord.utils import get

from Bot import CONFIG, save_config

LOGGER = logging.getLogger(__name__)


def get_channel(ctx, channel_id: int) -> Optional[GuildChannel]:
    return ctx.message.guild.get_channel(channel_id=channel_id)


class RoleCog(commands.Cog, name='Role Management'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Role',
        description='Add/Remove role/s to yourself',
        usage='[Role Names]'
    )
    async def edit_roles(self, ctx, *role_names: str):
        for role_name in role_names:
            role = get(ctx.author.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"`{role_name}` doesn't exist")
                continue
            if role.id in CONFIG['Ignored']:
                await ctx.send(f"`{role_name}` doesn't exist")
                continue
            if role.id in [x.id for x in ctx.author.roles]:
                await ctx.author.remove_roles(role)
            else:
                await ctx.author.add_roles(role)
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

    @commands.command(
        name='Blacklist',
        description='Add/Remove role/s to the unassignable list of roles',
        usage='[Role Names]'
    )
    async def blacklist_roles(self, ctx, *role_names: str):
        if CONFIG['Moderator'] not in [x.id for x in ctx.author.roles]:
            await ctx.send(f"{ctx.author.mention()}, you are not Authorized to use this command")
            await ctx.message.delete()
            return
        for role_name in role_names:
            role = get(ctx.author.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"`{role_name}` doesn't exist")
                continue
            if role.id in CONFIG['Ignored']:
                CONFIG['Ignored'].remove(role.id)
            else:
                CONFIG['Ignored'].append(role.id)
        save_config()
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

    @commands.command(
        name='List',
        description='List assignable roles'
    )
    async def list_roles(self, ctx):
        if CONFIG['Moderator'] not in [x.id for x in ctx.author.roles]:
            await ctx.send(f"{ctx.author.mention()}, you are not Authorized to use this command")
            await ctx.message.delete()
            return
        role_names = []
        for role in ctx.author.guild.roles:
            if role.id in CONFIG['Ignored']:
                continue
            role_names.append(role.name)
        role_str = '\n'.join(sorted(role_names))
        await ctx.send(f"```\n{role_str}```")
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(RoleCog(bot))
