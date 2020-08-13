from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    user_id: int                         # Discord User ID of muter
    hotkey: str = "|"                    # Trigger hotkey
    log_channel_id: Optional[int] = None # Log channel ID
    polling_sec: float = 0.05            # Keyboard polling interval
    command_prefix: str = "-"            # Command prefix
    role_name: str = "Among Us"          # Role-based muting (NYI)
    