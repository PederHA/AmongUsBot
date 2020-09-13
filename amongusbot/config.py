from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    user_id: int                            # ID of user to mute voice channel of
    hotkey: str = "|"                       # Trigger hotkey
    log_channel_id: Optional[int] = None    # Log channel ID
    poll_rate: float = 0.05                 # Keyboard polling rate (seconds)
    command_prefix: str = "-"               # Command prefix
    doubleclick: bool = False               # Require double-click of hotkey to trigger
    doubleclick_window: float = 0.5         # Double-click activation window (seconds)
    cooldown: float = 2.0                   # Trigger cooldown
    sound: bool = True                      # Play sound when triggered
    mute_sound: str = "audio/muted.wav"     # Mute sound
    unmute_sound: str = "audio/unmuted.wav" # Unmute sound

    def __post_init__(self) -> None:
        if self.sound:
            self.mute_sound = parse_sound_path(self.mute_sound)
            self.unmute_sound = parse_sound_path(self.unmute_sound)


def parse_sound_path(path: str) -> str:
    """Checks if path exists. Returns absolute path as string."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"{p} does not exist!")
    return str(p.absolute())
