import asyncio
import sys
import time
import traceback
from functools import partial
from pathlib import Path
from typing import Dict

import discord
import keyboard
from discord.ext import commands, tasks
from discord.utils import get

from .config import Config

# Platform-specific sound-playing module
# Only Windows is supported at the moment
if sys.platform == "win32":
    import winsound


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
        self.keyboard_loop._sleep = config.poll_rate
        self.doubleclick = config.doubleclick
        self.doubleclick_window = config.doubleclick_window
        self.cooldown = config.cooldown
        self.mute_sound = str(Path(config.mute_sound).absolute())
        self.unmute_sound = str(Path(config.unmute_sound).absolute())

        # State of voice channels the bot has modified. 
        self.voice_channels: Dict[int, bool] = {} # Key = Channel ID, Value: Is muted
        
        self.keyboard_loop.start()
        
    @tasks.loop(seconds=0.05)
    async def keyboard_loop(self) -> None:
        if keyboard.is_pressed(self.hotkey):
            # Double-click logic
            if self.doubleclick:
                start = time.time()
                # Wait until hotkey has been released
                while keyboard.is_pressed(self.hotkey):
                    await asyncio.sleep(0.01)
                # Poll keyboard for second keypress for a certain amount of time
                while (time.time() - start) < self.doubleclick_window:
                    if keyboard.is_pressed(self.hotkey):
                        break # Got second click
                    await asyncio.sleep(0.01)
                else:
                    return # Second click was not registered in time
            
            try:
                await self.toggle_mute(self.bot.get_user(self.user_id))
            except (TypeError, ValueError, discord.errors.Forbidden) as e:
                print("ERROR: ", e.args[0] if e.args else "") # TODO: Improve error reporting + logging
            await asyncio.sleep(self.cooldown) # Avoid accidentally triggering twice if hotkey is held down

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

        mute = not self.voice_channels[channel.id] # Inverse of current state
        for m in channel.members: # type: discord.Member
            await m.edit(mute=mute)
        await self.play_sound(mute)
        self.voice_channels[channel.id] = mute

    async def get_user_voice_channel(self, user: discord.User) -> discord.VoiceChannel:
        for guild in self.bot.guilds: # type: discord.Guild
            for ch in guild.voice_channels: # type: discord.VoiceChannel
                for member in ch.members: # type: discord.Member
                    if user.id == member.id:
                        return ch
        else:
            raise ValueError(f"Unable to find voice channel of {user.name}")

    async def play_sound(self, mute: bool) -> None:
        if sys.platform == "win32":
            await self._play_sound_windows(mute)
        
    async def _play_sound_windows(self, mute: bool) -> None:
        sound = self.mute_sound if mute else self.unmute_sound
        winsound.PlaySound(sound, winsound.SND_ASYNC)
