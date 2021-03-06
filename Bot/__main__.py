import logging

import discord
from discord.ext import commands

from Bot import CONFIG
from Logger import init_logger

LOGGER = logging.getLogger(__name__)
COGS = ['Bot.cogs.role_management']
bot = commands.Bot(command_prefix=commands.when_mentioned_or(CONFIG['Prefix']), case_insensitive=True)


@bot.event
async def on_ready():
    LOGGER.info(f"Logged in as: {bot.user}")
    bot.remove_command('help')
    for cog in COGS:
        bot.load_extension(cog)
    await bot.change_presence(activity=discord.Game(name='with Members roles'))


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)


if __name__ == "__main__":
    init_logger('Server-Manager')
    if CONFIG['Token']:
        bot.run(CONFIG['Token'], bot=True, reconnect=True)
    else:
        LOGGER.critical('Missing your Discord `Token`, update the config.yaml to continue')
