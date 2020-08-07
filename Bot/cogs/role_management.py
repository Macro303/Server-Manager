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
        if ctx.channel != get_channel(ctx, CONFIG['Channels']['Roles']) and \
                ctx.channel != get_channel(ctx, CONFIG['Channels']['Testing']):
            await ctx.message.delete()
            return
        for role_name in role_names:
            LOGGER.info(f"Trying to assign `{role_name}` to {ctx.author}")
            role = get(ctx.author.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"`{role_name}` does not exist")
                continue
            role_groups = []
            for x in CONFIG['Groups'].values():
                role_groups.extend(x)
            if role.id in [x for x in role_groups]:
                if role.id in [x.id for x in ctx.author.roles]:
                    await ctx.author.remove_roles(role)
                else:
                    await ctx.author.add_roles(role)
                await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
            else:
                await ctx.send(f"`{role_name}` does not exist")
                continue

    @commands.command(
        name='Add-Role',
        description='Create the assignable roles and give them a Group',
        usage='[Group] [Role Names]'
    )
    async def add_role(self, ctx, group: str, *role_names: str):
        if ctx.channel != get_channel(ctx, CONFIG['Channels']['Roles']) and \
                ctx.channel != get_channel(ctx, CONFIG['Channels']['Testing']):
            await ctx.message.delete()
            return
        LOGGER.info(f"Adding {role_names} to `{group}`")
        if 618596100332584970 not in [x.id for x in ctx.author.roles]:
            await ctx.send(f"{ctx.author.mention()}, you are not Authorized to use this command")
            await ctx.message.delete()
            return
        for role_name in role_names:
            role = get(ctx.author.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"`{role_name}` does not exist")
                continue
            if group in CONFIG['Groups']:
                CONFIG['Groups'][group] = list({*CONFIG['Groups'][group], role.id})
            else:
                CONFIG['Groups'][group] = [role.id]
            save_config()
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

    @commands.command(
        name='Del-Role',
        description='Remove assignable roles from the given Group',
        usage='[Group] [Role Names]'
    )
    async def del_role(self, ctx, group: str, *role_names: str):
        if ctx.channel != get_channel(ctx, CONFIG['Channels']['Roles']) and \
                ctx.channel != get_channel(ctx, CONFIG['Channels']['Testing']):
            await ctx.message.delete()
            return
        LOGGER.info(f"Removing {role_names} from `{group}`")
        if 618596100332584970 not in [x.id for x in ctx.author.roles]:
            await ctx.send(f"{ctx.author.mention()}, you are not Authorized to use this command")
            await ctx.message.delete()
            return
        for role_name in role_names:
            role = get(ctx.author.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"`{role_name}` does not exist")
                continue
            if group in CONFIG['Groups']:
                CONFIG['Groups'][group].remove(role.id)
            save_config()
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

    @commands.command(
        name='Roles',
        description='List assignable roles'
    )
    async def list_roles(self, ctx):
        if ctx.channel != get_channel(ctx, CONFIG['Channels']['Roles']) and \
                ctx.channel != get_channel(ctx, CONFIG['Channels']['Testing']):
            await ctx.message.delete()
            return
        LOGGER.info("Creating the Role Menu")
        if not CONFIG['Groups'].items():
            await ctx.send('No Roles found')
        for group, roles in CONFIG['Groups'].items():
            role_names = sorted(x.name for x in [get(ctx.author.guild.roles, id=role_id) for role_id in roles] if x)
            role_str = '\n'.join(role_names)
            await ctx.send(f"**__{group} Roles:__**\n```\n{role_str}```")
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(RoleCog(bot))
