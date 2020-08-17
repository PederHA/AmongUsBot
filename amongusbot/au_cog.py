import asyncio
import traceback
from typing import Dict, Optional

import discord
import keyboard
from discord.ext import commands, tasks
from discord.utils import get
from .config import Config


class AmongUsCog(commands.Cog):
    def __init__(
            self, 
            bot: commands.Bot,
            config: Config,
    ) -> None:
        self.bot = bot

        # Init config values
        self.user_id = config.user_id
        self.log_channel_id = config.log_channel_id
        self.hotkey = config.hotkey
        self.keyboard_loop._sleep = config.polling_sec

        # State of voice channels the bot has modified. 
        self.voice_channels: Dict[int, bool] = {} # Key = Channel ID, Value: Is muted
        
        self.keyboard_loop.start()
        
    @tasks.loop(seconds=0.05)
    async def keyboard_loop(self) -> None:
        if keyboard.is_pressed(self.hotkey):
            try:
                await self.toggle_mute(self.bot.get_user(self.user_id))
            except (TypeError, ValueError) as e:
                print(e.args[0] if e.args else "") # bad
            await asyncio.sleep(0.2) # Avoid double-click

    async def cog_command_error(self, ctx: commands.Context, exc: Exception) -> None:
        """This hardly qualifies as exception handling."""
        # Log traceback if logging is enabled and a log channel ID is specified
        if self.log_channel_id:
            channel = self.bot.get_channel(self.log_channel_id)
            await channel.send(traceback.format_exc(limit=1024))
        else:
            traceback.print_exc()
        
        # discord.py wraps exceptions, but we want the original exception message
        if hasattr(exc, "original"):
            exc = exc.original # type: ignore
        
        if exc.args:
            await ctx.send(f"ERROR: {exc.args[0]}")

    @commands.command(name="mute", aliases=["m"])
    async def mute(self, ctx: commands.Context) -> None:
        """Toggles muting of all users in your voice channel."""
        await self.toggle_mute(ctx.message.author)

    async def toggle_mute(self, user: discord.User) -> None:
        """Toggles server mute for every member in a user's voice channel."""
        if not user:
            raise TypeError("A user whose channel is to be (un)muted is required")

        channel = await self.get_user_voice_channel(user)
        if channel.id not in self.voice_channels:
            self.voice_channels[channel.id] = False # Mute = False

        state = not self.voice_channels[channel.id] # Inverse of current state
        for m in channel.members: # type: discord.Member
            await m.edit(mute=state)
        self.voice_channels[channel.id] = state

    async def get_user_voice_channel(self, user: discord.User) -> discord.VoiceChannel:
        for ch in self.bot.get_all_channels(): # type: discord.VoiceChannel
            if not isinstance(ch, discord.VoiceChannel):
                continue
            for member in ch.members: # type: discord.Member
                if user.id == member.id:
                    return ch
        else:
            raise ValueError(f"Unable to find voice channel of {user.name}")
        