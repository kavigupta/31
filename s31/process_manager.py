import os
from datetime import timedelta
import signal
import time

from display_timedelta import display_timedelta

from .active_process_table import active_process_table
from .interruptable_runner import clean_table


def load_processes(prefix, ordering):
    with active_process_table() as t:
        clean_table(t)
        t = dict(t.items())
    if prefix is not None:
        t = {k: v for k, v in t.items() if v["name"].startswith(prefix)}
    return sorted(t.values(), key=lambda x: x[ordering])


def list_procesess(prefix, ordering):
    processes = load_processes(prefix, ordering)
    with_prefix = f"with prefix {prefix!r} " if prefix is not None else ""
    print(f"Active processes {with_prefix}({len(processes)}):")
    for proc in processes:
        print(render(proc))


def render(proc):
    return f"- {proc['name']} ({proc['pid']}) [started {display_timedelta(timedelta(seconds=time.time() - proc['timestamp']))} ago] {{{proc['cmd']}}}"


def stop_process(name):
    if len(name) == 0:
        print("No process name specified")
        return 1
    with_name_prefix = load_processes(name, "timestamp")
    if len(with_name_prefix) == 0:
        print(f"No process with name {name} found")
        return 1
    if len(with_name_prefix) > 1:
        print(f"Multiple processes with prefix {name} found:")
        for proc in with_name_prefix:
            print(render(proc))
        if input("Do you want to stop all of them? [y/N] ") != "y":
            print("Aborting")
            return 1
        for proc in with_name_prefix:
            stop(proc)
        return 0
    proc = with_name_prefix[0]
    if proc["name"] != name:
        print(
            f"Process name {proc['name']} does not match {name}. Please type the full name."
        )
        return 1
    stop(proc)
    return 0

def stop(proc):
    print(f"Stopping {render(proc)}")
    os.kill(proc["pid"], signal.SIGINT)
