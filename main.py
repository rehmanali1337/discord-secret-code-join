import discord
from discord.ext import commands
import config
import os
import sys
import asyncio
from app import (
    logger,
    Console
)
from app.state import State


if "linux" in sys.platform:
    logger.debug("Installing uvloop to increase performance")
    import uvloop
    uvloop.install()

elif "win" in sys.platform:
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)
    logger.debug("Setting the title of the command prompt")
    # os.system(f"title {config.DATABASE_NAME} - Bot")

intents = discord.Intents.all()
bot = commands.AutoShardedBot(
    command_prefix=config.COMMAND_PREFIX,
    intents=intents,
    fetch_offline_members=True)


def cogs_list(cog_folder):
    files = list(os.walk(cog_folder))[0][2]
    return [cog.split(".")[0] for cog in files if cog != "__init__.py"]


@bot.event
async def on_ready():
    await State.setup()
    exts = cogs_list("cogs")
    for ext in exts:
        try:
            bot.load_extension(f'cogs.{ext}')
        except commands.errors.ExtensionNotLoaded:
            Console.warn(f'{ext} could not be loaded!')
        except Exception as e:
            logger.debug(
                f"unhandled exception while loading extension {e}", exc_info=True)
            continue
    print(f"Logged in as {bot.user}")

if __name__ == '__main__':
    bot.run(config.BOT_TOKEN)
