#!/usr/bin/env python3
import logging

from discord import Embed
from discord.ext import commands

from Bot import CONFIG

LOGGER = logging.getLogger(__name__)


class AdminCog(commands.Cog, name='Other Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Help',
        description='The help command'
    )
    async def help_command(self, ctx):
        embed = Embed(title='Server Manager Commands')
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        cogs = [c for c in self.bot.cogs.keys()]
        for cog in cogs:
            cog_commands = self.bot.get_cog(cog).get_commands()
            commands_list = []
            for comm in cog_commands:
                usage = f"{CONFIG['Prefix']}{comm.name} {comm.usage or ''}".strip()
                commands_list.append(f"**{comm.name}** - `{usage}`\n*{comm.description}*")

            embed.add_field(name=cog, value='\n'.join(commands_list), inline=False)

        embed.set_footer(
            text=f"Requested by {ctx.message.author.name}",
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=embed)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(AdminCog(bot))
