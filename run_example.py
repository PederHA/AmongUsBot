import os
import sys

from amongusbot import run, Config


def main() -> None:
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = os.environ.get("AUBOT_TOKEN")
    # Only user_id is required. 
    # All other parameters can be omitted.
    config = Config(
        user_id=123456,
        hotkey="f1", 
        log_channel_id=234567, 
        poll_rate=0.5
    )
    run(token, config)


if __name__ == "__main__":
    main()
