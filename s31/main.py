import argparse
import sys
import os
import json

from .config import Config, update_config
from .notify import notify
from .command import Command
from .foreach import MAX_FOREACHES, parse_foreach_args, parse_values
from .utils import format_assignments, sanitize, set_key
from .workers import dispatch_workers


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
    command_parser.add_argument(
        "-fw",
        "--foreach-worker",
        nargs=2,
        metavar=("%var", "vals"),
        action="append",
        help="Similar to -f but associates each substitution with a particular variable. "
        "Notably, this does not lead to a combinatoric explosion if multiple are used, they are "
        "implicitly zipped together by the worker index",
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
    command_parser.add_argument(
        "-w",
        "--max-workers",
        type=int,
        help="Limit the number of threads that are to be launched at any point. "
        "This forces the creation of a monitoring thread, for which --sync is applied to",
    )
    command_parser.add_argument(
        "-wn",
        "--worker-monitor-name",
        default="worker-monitor",
        help="Names the screen for the worker thread. By default is 'worker-monitor'",
    )
    # internal use only, specifies that when the process is done, it should set the given key of the given file.
    command_parser.add_argument(
        "--when-done-set", nargs=2, metavar=("file", "key"), help=argparse.SUPPRESS
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
    try:
        return do_command_action(args)
    finally:
        if args.when_done_set is not None:
            set_key(*args.when_done_set)


def do_command_action(args):
    config = Config(args.config_file)
    assignments = (
        [args.foreach_specified_args]
        if args.foreach_specified_args is not None
        else parse_foreach_args(args)
    )
    worker_assignments = []
    # Validation
    if args.foreach_worker is not None:
        for variable, vals in args.foreach_worker:
            if args.max_workers is None:
                raise RuntimeError("Cannot provide -fw without -w")
            vals = parse_values(vals)
            if len(vals) != args.max_workers:
                raise RuntimeError(
                    "Mismatch between number of workers and number of provided values"
                )
            worker_assignments.append((variable, vals))

    commands = []
    for assignment in assignments:
        screen_name = sanitize(
            format_assignments(args.screen_name or args.command, assignment)
        )
        cmd = Command(cmd_line=args.command, location=args.location)
        cmd_to_use = cmd.replace(assignment)
        commands.append((screen_name, cmd_to_use, assignment))

    if args.dry_run:
        for screen_name, cmd_to_use, _ in commands:
            if not args.sync:
                print("# on screen {}".format(screen_name))
            cmd_to_use.dry_run()
        return

    if not args.sync:
        if args.max_workers is not None:
            config.launch_screen(sys.argv + ["--sync"], args.worker_monitor_name)
            return
        for screen_name, _, assignment in commands:
            config.launch_screen(
                sys.argv
                + ["--sync", "--foreach-specified-args", json.dumps(assignment)],
                screen_name,
            )
        return

    if args.max_workers is not None and args.foreach_specified_args is None:
        # if foreach-specified-args is set, this is a dispatch thread
        def launch_worker(worker_idx, assignment, output_file, token):
            assignment = assignment + [
                (var, vals[worker_idx]) for var, vals in worker_assignments
            ]
            screen_name = sanitize(
                format_assignments(args.screen_name or args.command, assignment)
            )
            print("Launching {}".format(screen_name))
            # don't need the --sync since at this point it is guaranteed
            config.launch_screen(
                sys.argv
                + [
                    "--foreach-specified-args",
                    json.dumps(assignment),
                    "--when-done-set",
                    output_file,
                    token,
                ],
                screen_name,
            )

        dispatch_workers(args.max_workers, launch_worker, assignments)
        return

    for _, cmd_to_use, _ in commands:
        if args.no_email:
            cmd_to_use.run()
        else:
            notify(config, cmd_to_use)


def config_action(args):
    update_config(args.config_file, {args.key: args.value})
