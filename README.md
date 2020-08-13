# AmongUsBot

Shitty bot that toggles server muting of all members in a specific user's voice channel when a hotkey is pressed. Uses the [`keyboard`](https://pypi.org/project/keyboard/) module to listen for keypresses. 

## Installation

Clone the repository and run:
```
poetry install
```

## Usage

Press the hotkey whenever a round starts to mute everyone in your channel, and press it again whenever a meeting is convened or the game ends.

### Configuration

`amongusbot/config.py` defines the following datastructure:
```python
@dataclass
class Config:
    user_id: int                         # Discord User ID of muter
    hotkey: str = "|"                    # Trigger hotkey
    log_channel_id: Optional[int] = None # Log channel ID
    polling_sec: float = 0.05            # Keyboard polling interval
    command_prefix: str = "-"            # Command prefix
    role_name: str = "Among Us"          # Role-based muting (NYI)
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
