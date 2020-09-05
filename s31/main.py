import argparse
import sys
import os

from .config import Config, update_config
from .notify import notify
from .command import Command


def main():
    def config_argument(p):
        p.add_argument(
            "--config-file",
            default=os.path.expanduser("~/.31rc"),
            help="The location of the configuration file",
        )

    parser = argparse.ArgumentParser("31")
    subparsers = parser.add_subparsers(dest="cmd")
    subparsers.required = True

    command_parser = subparsers.add_parser(
        "command", help="Run a command", aliases=["c"]
    )
    config_argument(command_parser)
    command_parser.add_argument(
        "-s",
        "--sync",
        action="store_true",
        help="Run the command synchronously, that is, not in a screen session",
    )
    command_parser.add_argument(
        "-n", "--screen-name", help="The name of the screen session to create"
    )
    command_parser.add_argument(
        "-l", "--location", help="The location to run the script"
    )
    command_parser.add_argument(
        "--no-email",
        help="Do not send an email when the command is done running",
        action="store_true",
    )
    command_parser.add_argument("command", help="Command to run")
    command_parser.set_defaults(action=command_action)

    config_parser = subparsers.add_parser("config", help="Modify configuration")
    config_argument(config_parser)
    config_parser.add_argument("key", help="The configuration key to modify")
    config_parser.add_argument("value", help="The value to assign the given key to")
    config_parser.set_defaults(action=config_action)
    args = parser.parse_args()

    try:
        args.action(args)
    except RuntimeError as e:
        print(e, file=sys.stderr)


def command_action(args):
    config = Config(args.config_file)
    if args.sync:
        cmd = Command(cmd_line=args.command, location=args.location)
        if args.no_email:
            cmd.run()
        else:
            notify(config, cmd)
    else:
        config.launch_screen(sys.argv + ["--sync"], args.screen_name or args.command)


def config_action(args):
    update_config(args.config_file, {args.key: args.value})
