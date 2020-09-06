import argparse
import sys
import os
import json

from .config import Config, update_config
from .notify import notify
from .command import Command
from .foreach import MAX_FOREACHES, parse_foreach_args
from .utils import format_assignments, sanitize


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
    command_parser.add_argument(
        "-d",
        "--dry-run",
        help="Print out the commands to be run rather than running them",
        action="store_true",
    )
    command_parser.add_argument(
        "-f",
        "--foreach",
        metavar=("%var", "vals"),
        nargs=2,
        action="append",
        help="Replaces each occurence of the variable with the corresponding value. "
        "Variables can be any sequence of characters. "
        "After the variables, values can be provided, each list of values should be a single argument in CSV format. "
        "See the documentation for details and examples.",
    )
    for k in range(2, 1 + MAX_FOREACHES):
        meta = tuple("%var{}".format(i) for i in range(1, k + 1))
        meta += tuple("vals{}".format(i) for i in range(1, k + 1))
        command_parser.add_argument(
            "-f" + str(k),
            "--foreach-" + str(k),
            metavar=meta,
            nargs=k * 2,
            action="append",
            help="See -f for details, -f2 through -f{0} allow you to zip the values for 2-{0} variables together.".format(
                MAX_FOREACHES
            )
            if k == 2
            else argparse.SUPPRESS,
        )
    # internal use only, specifies which foreach args to use, in json format [(name, value)]
    command_parser.add_argument(
        "--foreach-specified-args", type=json.loads, help=argparse.SUPPRESS
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
    assignments = (
        [args.foreach_specified_args]
        if args.foreach_specified_args is not None
        else parse_foreach_args(args)
    )
    for assignment in assignments:
        screen_name = sanitize(
            format_assignments(args.screen_name or args.command, assignment)
        )
        if args.sync or args.dry_run:
            cmd = Command(cmd_line=args.command, location=args.location)
            cmd_to_use = cmd.replace(assignment)
            if args.dry_run:
                if not args.sync:
                    print("# on screen {}".format(screen_name))
                cmd_to_use.dry_run()
            elif args.no_email:
                cmd_to_use.run()
            else:
                notify(config, cmd_to_use)
        else:
            config.launch_screen(
                sys.argv
                + ["--sync", "--foreach-specified-args", json.dumps(assignment)],
                screen_name,
            )


def config_action(args):
    update_config(args.config_file, {args.key: args.value})
