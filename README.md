# AmongUsBot

Shitty bot that toggles server muting of all members in a specific user's voice channel when a hotkey is pressed. Uses the [`keyboard`](https://pypi.org/project/keyboard/) module to listen for keypresses.

## Installation

Clone the repository and install with [Poetry](https://python-poetry.org/):

```bash
git clone https://github.com/PederHA/AmongUsBot.git
cd amongusbot
poetry install
```

Alternatively:

```bash
pip install https://github.com/PederHA/AmongUsBot/releases/download/0.2.0/amongusbot-0.2.0.tar.gz
```

## Usage

Press the hotkey whenever a round starts to mute everyone in your channel, and press it again whenever a meeting is convened or the game ends.

### Configuration

`amongusbot/config.py` defines the following configuration options:

```python
@dataclass
class Config:
    user_id: int                            # Discord ID of user's channel to mute
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
```

Defaults can be overriden when running the bot:

```python
from amongusbot import run, Config

run("your_token", Config(user_id=123456, hotkey="f4"))
```

### Running

See `run_example.py`.

When inviting the bot to your server, use the following permissions integer: `12962880`

## Notes

Only tested on Windows.