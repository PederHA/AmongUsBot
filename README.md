# AmongUsBot

Shitty (but lightweight) bot that toggles server muting of all members in a specific user's voice channel when a hotkey is pressed. Uses the [`keyboard`](https://pypi.org/project/keyboard/) module to listen for keypresses. 

If you are looking for the project with the same very original name that uses Tesseract and Selenium go here: https://github.com/alpharaoh/AmongUsBot

## Installation

### Clone the Repository and Install with [Poetry](https://python-poetry.org/) (preferred)

```bash
git clone https://github.com/PederHA/AmongUsBot.git
cd amongusbot
poetry install
```

### Install with pip (alternative)

```bash
pip install amongusbot
```

NOTE: The version on PyPi does not include sound alerts and example run file! Download those files manually and place them in your project root if you choose to use pip.

## Running

### Create a Bot User

Go to https://discord.com/developers/applications and create a new application, then add a bot user to the application by clicking on the "Bot" tab on the left-hand side of the page.

### Invite the Bot to Your Server

Invite the bot with the following URL (substitute with your bot's ID):
`https://discord.com/oauth2/authorize?client_id=<BOT_CLIENT_ID>&scope=bot&permissions=12651520`

### Run the Bot

See `run_example.py`.

Add the bot's secret token as an environment variable named `AUBOT_TOKEN` or pass it in as the first argument to the application when running it.

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

Defaults can be overridden when running the bot:

```python
from amongusbot import run, Config

run("your_token", Config(user_id=123456, hotkey="f4"))
```

## Usage

Press the hotkey whenever a round starts to mute everyone in your channel, and press it again whenever a meeting is convened or the game ends.

## Notes

Only tested on Windows.
