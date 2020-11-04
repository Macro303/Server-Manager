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

    async def is_authorized(self, ctx) -> bool:
        if CONFIG['Moderator']:
            authorized = False
            for role_id in CONFIG['Moderator']:
                if role_id in [x.id for x in ctx.author.roles]:
                    authorized = True
            if not authorized:
                await ctx.send(f"{ctx.author.mention()}, you are not Authorized to use this command")
                await ctx.message.delete()
                return False
        return True

    @commands.command(name='Role')
    async def roles(self, ctx, *role_names: str):
        if len(role_names) == 0:
            await self.list_roles(ctx)
        else:
            await self.edit_roles(ctx, *role_names)

    async def list_roles(self, ctx):
        if not await self.is_authorized(ctx):
            return
        LOGGER.info(f"{ctx.author} is displaying the Roles")
        role_names = []
        for role in ctx.author.guild.roles:
            if role.id in CONFIG['Blacklist']:
                continue
            role_names.append(role.name)
        role_str = '\n'.join(sorted(role_names))
        await ctx.send(f"```\n{role_str}```")
        await ctx.message.delete()

    async def edit_roles(self, ctx, *role_names: str):
        LOGGER.info(f"{ctx.author} is editing their Roles")
        for role_name in role_names:
            role = get(ctx.author.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"`{role_name}` doesn't exist")
                continue
            if role.id in CONFIG['Blacklist']:
                await ctx.send(f"`{role.name}` doesn't exist")
                continue
            if role.id in [x.id for x in ctx.author.roles]:
                await ctx.author.remove_roles(role)
                await ctx.send(f"Took `{role.name}` from {ctx.author.display_name}")
            else:
                await ctx.author.add_roles(role)
                await ctx.send(f"Gave `{role.name}` to {ctx.author.display_name}")
        await ctx.message.delete()

    @commands.command(name='Blacklist')
    async def blacklist(self, ctx, *role_names: str):
        if not await self.is_authorized(ctx):
            return
        if len(role_names) == 0:
            await self.list_blacklist(ctx)
        else:
            await self.edit_blacklist(ctx, *role_names)

    async def list_blacklist(self, ctx):
        LOGGER.info(f"{ctx.author} is displaying the Blacklist")
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

    async def edit_blacklist(self, ctx, *role_names: str):
        LOGGER.info(f"{ctx.author} is editing the Blacklist")
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
    bot.add_cog(RoleCog(bot))
