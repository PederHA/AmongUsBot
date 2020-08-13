from typing import Optional

import discord
from discord.ext.commands import Bot

from .au_cog import AmongUsCog
from .config import Config


def run(token: str, config: Config) -> None:
    bot = Bot(command_prefix=config.command_prefix)
    bot.add_cog(
        AmongUsCog(bot, config)
    )
    bot.run(token)
