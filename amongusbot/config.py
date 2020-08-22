from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    user_id: int                         # Discord ID of user's channel to mute
    hotkey: str = "|"                    # Trigger hotkey
    log_channel_id: Optional[int] = None # Log channel ID
    poll_rate: float = 0.05              # Keyboard polling rate (seconds)
    command_prefix: str = "-"            # Command prefix
    doubleclick: bool = False            # Require double-click of hotkey to trigger
    doubleclick_window: float = 0.5      # Double-click activation window (seconds)
    cooldown: float = 1.0                # (Un)mute cooldown