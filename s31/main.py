import argparse
import sys

from .config import Config, update_config
from .notify import notify


def main():
    parser = argparse.ArgumentParser("31")
    parser.add_argument("-c", "--command", help="The command to run")
    parser.add_argument(
        "-s",
        "--sync",
        action="store_true",
        help="Run the command synchronously, that is not in a screen session",
    )
    parser.add_argument(
        "-n", "--screen-name", help="The name of the screen session to create"
    )
    parser.add_argument(
        "--config",
        nargs="+",
        help="Pass in configuration arguments to set in the form --config key1 value1 key2 value2 ...",
    )
    args = parser.parse_args()

    try:
        run_command(args)
    except RuntimeError as e:
        print(e, file=sys.stderr)


def run_command(args):
    if (args.command is not None) == (args.config is not None):
        raise RuntimeError(
            "Must provide exactly one of (1) a command to run via -c or (2) configuration setup via --config"
        )

    if args.config is not None:
        if len(args.config) % 2 != 0:
            raise RuntimeError(
                "Unmatched key/value pair in configuration: " + args.config[-1]
            )
        new_config = {
            args.config[i]: args.config[i + 1] for i in range(0, len(args.config), 2)
        }
        update_config(new_config)
        return

    config = Config()
    if args.sync:
        notify(config, args.command)
    else:
        config.launch_screen(sys.argv + ["--sync"], args.screen_name or args.command)
