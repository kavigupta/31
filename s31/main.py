import argparse
import sys

from .config import Config, update_config
from .notify import notify


def main():
    parser = argparse.ArgumentParser("31")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-c", "--command", help="The command to run")
    parser.add_argument(
        "-s",
        "--sync",
        action="store_true",
        help="Run the command synchronously, that is not in a screen session",
    )
    parser.add_argument(
        "-n", "--screen-name", help="The name of the screen session to create"
    )
    group.add_argument(
        "--config",
        nargs=2,
        metavar=("key", "value"),
        help="Edit a configuration argument",
    )
    args = parser.parse_args()

    try:
        run_command(args)
    except RuntimeError as e:
        print(e, file=sys.stderr)


def run_command(args):
    if args.config is not None:
        update_config({args.config[0] : args.config[1]})
        return

    config = Config()
    if args.sync:
        notify(config, args.command)
    else:
        config.launch_screen(sys.argv + ["--sync"], args.screen_name or args.command)
