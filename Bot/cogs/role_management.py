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
        description='Assign/Remove a role to yourself',
        usage='[Role Names]'
    )
    async def assign_role(self, ctx, *role_names: str):
        if ctx.channel != get_channel(ctx, CONFIG['Channels']['Requests']) and \
                ctx.channel != get_channel(ctx, CONFIG['Channels']['Testing']):
            await ctx.message.delete()
            return
        for role_name in role_names:
            LOGGER.info(f"Trying to assign `{role_name}` to {ctx.author}")
            role = get(ctx.author.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"`{role_name}` does not exist")
                continue
            if role.id in [x for x in CONFIG['Roles']]:
                if role.id in [x.id for x in ctx.author.roles]:
                    await ctx.author.remove_roles(role)
                else:
                    await ctx.author.add_roles(role)
                await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
            else:
                await ctx.send(f"`{role_name}` does not exist")
                continue

    @commands.command(
        name='Edit-Roles',
        description='Add/Remove role/s to the list of assignable roles',
        usage='[Role Names]'
    )
    async def add_role(self, ctx, *role_names: str):
        if ctx.channel != get_channel(ctx, CONFIG['Channels']['Requests']) and \
                ctx.channel != get_channel(ctx, CONFIG['Channels']['Testing']):
            await ctx.message.delete()
            return
        LOGGER.info(f"Adding/Removing {role_names}")
        if CONFIG['Admin Role'] not in [x.id for x in ctx.author.roles]:
            await ctx.send(f"{ctx.author.mention()}, you are not Authorized to use this command")
            await ctx.message.delete()
            return
        for role_name in role_names:
            role = get(ctx.author.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"`{role_name}` does not exist")
                continue
            if role.id in CONFIG['Roles']:
                CONFIG['Roles'].remove(role.id)
            else:
                CONFIG['Roles'].append(role.id)
            save_config()
            await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

    @commands.command(
        name='Roles',
        description='List assignable roles'
    )
    async def list_roles(self, ctx):
        if ctx.channel != get_channel(ctx, CONFIG['Channels']['Requests']) and \
                ctx.channel != get_channel(ctx, CONFIG['Channels']['Testing']):
            await ctx.message.delete()
            return
        LOGGER.info('Listing assignable roles')
        if not CONFIG['Roles']:
            await ctx.send('No Roles found')
        role_names = sorted(x.name for x in [get(ctx.author.guild.roles, id=role_id) for role_id in CONFIG['Roles']] if x)
        role_str = '\n'.join(role_names)
        await ctx.send(f"```\n{role_str}```")
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(RoleCog(bot))
