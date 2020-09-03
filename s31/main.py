import argparse
import sys

from .config import Config, update_config
from .notify import notify


def main():
    parser = argparse.ArgumentParser("31")
    subparsers = parser.add_subparsers(required=True, dest="cmd")

    command_parser = subparsers.add_parser(
        "command", help="Run a command", aliases=["c"]
    )
    command_parser.add_argument(
        "-s",
        "--sync",
        action="store_true",
        help="Run the command synchronously, that is not in a screen session",
    )
    command_parser.add_argument(
        "-n", "--screen-name", help="The name of the screen session to create"
    )
    command_parser.add_argument("command", help="Command to run")
    command_parser.set_defaults(action=command_action)

    config_parser = subparsers.add_parser("config", help="Modify configuration")
    config_parser.add_argument("key", help="The configuration key to modify")
    config_parser.add_argument("value", help="The value to assign the given key to")
    config_parser.set_defaults(action=config_action)
    args = parser.parse_args()

    try:
        args.action(args)
    except RuntimeError as e:
        print(e, file=sys.stderr)


def command_action(args):
    config = Config()
    if args.sync:
        notify(config, args.command)
    else:
        config.launch_screen(sys.argv + ["--sync"], args.screen_name or args.command)


def config_action(args):
    update_config({args.key: args.value})
