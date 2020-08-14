

import asyncio
import traceback
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Optional, DefaultDict, List
import time

import discord
import keyboard
from discord.ext import commands, tasks
from discord.utils import get
from .config import Config

StatusType = DefaultDict[int, DefaultDict[int, Member]]

@dataclass
class Member:
    member: discord.Member = None  
    role: discord.Role = None
    last_active: float = 0.0
    
    def __bool__(self) -> bool:
        if not self.member:
            return False
        for role in self.member.roles:
            if self.role == role:
                return True
        return False


class MemberStatus:
    def __init__(self) -> None:
        # State of users in guilds. 
        # Key: Guild ID, Value: {Key: User ID, Value: Has role}
        self._status: StatusType = defaultdict(lambda: defaultdict(Member))

    async def get(self, guild_id: int, user_id: int) -> Member:
        """Retrieves a Member. 

        Returns default Member, whose bool(member) evaluates to false, 
        if Member does not exist."""
        return self._status[guild_id][user_id]

    async def set(self, member: discord.Member, role: discord.Role) -> None:
        """Creates a new entry for a member."""
        self._status[member.guild.id][member.id] = Member(member, role, time.time())

    async def update(self, member: discord.Member) -> None:
        """Updates a member's last active time."""
        self._status[member.guild.id][member.id].last_active = time.time()

    async def purge(self, bot: commands.Bot, guild: discord.Guild, role: discord.Role) -> None:
        for member in guild.members: # type: discord.Member
            member.remove_roles(role)
        self._status.pop(guild.id)


class ChannelStatus:
    """Stores whether or not the Among us role can speak in a specific channel."""
    def __init__(self) -> None:
        self._status: DefaultDict[int, bool] = defaultdict(lambda: not bool()) # default=True

    async def toggle(self, channel: discord.VoiceChannel, role: discord.Role) -> None:
        can_speak = not self._status[channel.id] # inverse of current
        await channel.set_permissions(role, speak=can_speak)
        self._status[channel.id] = can_speak


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
        self.role_name = config.role_name
        self.keyboard_loop._sleep = config.polling_sec

        # State of voice channels the bot has modified. 
        self.voice_channels: Dict[int, bool] = {} # Key: Channel ID, Value: Can speak
        
        # State of users in guilds. 
        # Key: Guild ID, Value: {Key: User ID, Value: Has role}
        self.members = MemberStatus()
        self.channels = ChannelStatus()

        self.init_voice_channels()
        self.keyboard_loop.start()
        
    @tasks.loop(seconds=0.05)
    async def keyboard_loop(self) -> None:
        """Polls to check if the mute hotkey is pressed."""
        if keyboard.is_pressed(self.hotkey):
            try:
                await self.toggle_mute(self.bot.get_user(self.user_id))
            except (TypeError, ValueError) as e:
                print(e.args[0] if e.args else "") # bad
            await asyncio.sleep(0.2) # Avoid double-click

    @tasks.loop(minutes=30)
    async def remove_roles_loop(self) -> None:
        """Periodically makes sure all empty channels with existing Among Us role 
        rules allow the Among Us role to speak."""
        await self.init_channels(nonempty_ok=False)

    async def init_channels(self, nonempty_ok: bool=True) -> None:
        """Gives the Among Us role speaking privileges in all channels
        that have existing Among Us privileges.
        
        Useful if the bot crashes or is shut down while the Among Us role
        has its speaking privileges revoked from a channel.
        """
        for guild in self.bot.guilds: # type: discord.Guild
            role = get(self.role_name)
            if not role:
                continue
            for channel in guild.voice_channels: # type: discord.VoiceChannel
                if nonempty_ok or len(channel.members) == 0:
                    channel.set_permissions(role, speak=True)        

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
        """
        Toggles the speaking privileges of the Among Us role in a user's
        voice channel.
        """
        if not user:
            raise TypeError("A user whose channel is to be (un)muted is required")

        channel = await self.get_user_voice_channel(user)

        role = await self.get_role(channel)
        if not role:
            raise AttributeError(f'Unable to find the "{self.role_name}" role. Create this role and apply it to players.')
        
        # Make sure every member in the voice channel has the Among Us role
        await self.set_members_role(channel.members, role)
        
        # Toggle speaking ability in channel on/off
        await self.channels.toggle(channel, role)

    async def get_user_voice_channel(self, user: discord.User) -> discord.VoiceChannel:
        for guild in self.bot.guilds: # type: discord.Guild
            for ch in guild.voice_channels: # type: discord.VoiceChannel
                for member in ch.members: # type: discord.Member
                    if user.id == member.id:
                        return ch
        else:
            raise ValueError(f"Unable to find voice channel of {user.name}")
    
    async def get_role(self, channel: discord.VoiceChannel) -> Optional[discord.Role]:
        """Attempts to find a role with the config-defined role name."""
        return get(channel.guild.roles, name=self.role_name)

    async def set_members_role(self, members: List[discord.Member], role: discord.Role) -> None:
        """Adds the role to the User if the user does not already have the role."""
        for member in members:
            # FIXME: Double memory allocation if member doesn't exist due to using defaultdict
            if not self.status.get(member.guild.id, member.id):
                await member.add_roles(role)
                await self.members.set(member, role)
            else:
                await self.members.update(member)
