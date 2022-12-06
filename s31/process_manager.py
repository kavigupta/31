import os
from datetime import timedelta
import signal
import time

from display_timedelta import display_timedelta

from .active_process_table import active_process_table
from .interruptable_runner import clean_table


def load_processes(ordering):
    with active_process_table() as t:
        clean_table(t)
        t = dict(t.items())
    return sorted(t.values(), key=lambda x: x[ordering])


def list_procesess(ordering):
    processes = load_processes(ordering)
    print(f"Active processes ({len(processes)}):")
    for proc in processes:
        print(render(proc))


def render(proc):
    return f"- {proc['name']} ({proc['pid']}) [started {display_timedelta(timedelta(seconds=time.time() - proc['timestamp']))} ago] {{{proc['cmd']}}}"


def stop_process(name):
    if len(name) == 0:
        print("No process name specified")
        return 1
    processes = load_processes("timestamp")
    with_name_prefix = [p for p in processes if p["name"].startswith(name)]
    if len(with_name_prefix) == 0:
        print(f"No process with name {name} found")
        return 1
    if len(with_name_prefix) > 1:
        print(f"Multiple processes with prefix {name} found:")
        for proc in with_name_prefix:
            print(render(proc))
        return 1
    proc = with_name_prefix[0]
    if proc["name"] != name:
        print(
            f"Process name {proc['name']} does not match {name}. Please type the full name."
        )
        return 1
    print(f"Stopping {render(proc)}")
    os.kill(proc["pid"], signal.SIGINT)
    return 0
