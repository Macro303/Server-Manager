import logging
from typing import Optional

from discord.abc import GuildChannel
from discord.ext.commands import Cog, group, command, has_role
from discord.utils import get

from Bot import CONFIG, save_config

LOGGER = logging.getLogger(__name__)


def get_channel(ctx, channel_id: int) -> Optional[GuildChannel]:
    return ctx.message.guild.get_channel(channel_id=channel_id)


class RolesCog(Cog, name='Role Management'):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='Role',
        pass_context=True,
        usage=''
    )
    async def list_roles(self, ctx):
        role_names = []
        for role in ctx.author.guild.roles:
            if role.id in CONFIG['Blacklist']:
                continue
            role_names.append(role.name)
        role_str = '\n'.join(sorted(role_names))
        await ctx.send(f"```\n{role_str}```")
        await ctx.message.delete()
    

    @command(
        name='Role',
        pass_context=True,
        usage='[<RoleName>]'
    )
    async def edit_roles(self, ctx, *role_names: str):
        for role_name in role_names:
            role = get(ctx.author.guild.roles, name=role_name)
            if not role or role.id in CONFIG['Blacklist']:
                await ctx.send(f"`{role_name}` doesn't exist")
                continue
            if role.id in [x.id for x in ctx.author.roles]:
                await ctx.author.remove_roles(role)
                await ctx.send(f"Took `{role.name}` from {ctx.author.display_name}")
            else:
                await ctx.author.add_roles(role)
                await ctx.send(f"Gave `{role.name}` to {ctx.author.display_name}")
        await ctx.message.delete()

    @command(
        name='Blacklist',
        pass_context=True,
        usage=''
    )
    @has_role('Moderator')
    async def list_blacklist(self, ctx):
        role_names = {}
        for role_id in CONFIG['Blacklist']:
            role = get(ctx.author.guild.roles, id=role_id)
            if not role:
                CONFIG['Blacklist'].remove(role_id)
                continue
            role_names[role.id] = role.name
        role_names = [f"{k}: {v}" for k, v in sorted(role_names.items(), key=lambda item: item[1])]
        role_str = '\n'.join(role_names)
        await ctx.send(f"```\n{role_str}```")
        await ctx.message.delete()
    

    @command(
        name='Blacklist',
        pass_context=True,
        usage='[<RoleName>]'
    )
    @has_role('Moderator')
    async def edit_blacklist(self, ctx, *role_names: str):
        for role_name in role_names:
            role = get(ctx.author.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"`{role_name}` doesn't exist")
                continue
            if role.id in CONFIG['Blacklist']:
                CONFIG['Blacklist'].remove(role.id)
                await ctx.send(f"Removed `{role.name}` from the Blacklist")
            else:
                CONFIG['Blacklist'].append(role.id)
                await ctx.send(f"Added `{role.name}` to the Blacklist")
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(RolesCog(bot))
