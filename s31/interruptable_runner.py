import time
import uuid
import threading
import random

from .active_process_table import active_process_table


INTERRUPTED_BANNER = """
=======================================
INTERRUPTED BY USER
=======================================
"""

POLL_INTERVAL = 2


class InterruptableRunner:
    def __init__(self, name, pid, cmd_to_use):
        self.name = name
        self.pid = pid
        self.cmd_to_use = cmd_to_use
        self.guid = str(uuid.uuid4())
        self.timestamp = time.time()
        self.alive = False

    def pre(self):
        with active_process_table() as t:
            t[self.guid] = dict(
                name=self.name,
                pid=self.pid,
                cmd=self.cmd_to_use.cmd_line,
                timestamp=self.timestamp,
                last_update=self.timestamp,
            )
        self.alive = True
        while_alive_thread = threading.Thread(target=self.while_alive)
        while_alive_thread.start()

    def post(self):
        self.alive = False
        with active_process_table() as t:
            del t[self.guid]

    def while_alive(self):
        while self.alive:
            with active_process_table() as t:
                if self.guid in t:
                    val = t[self.guid]
                    val["last_update"] = time.time()
                    t[self.guid] = val
            time.sleep(random.uniform(0.5 * POLL_INTERVAL, 1.5 * POLL_INTERVAL))

    def run_checking_interrupt(self, fn, interrupted_banner_path=None):
        try:
            self.pre()
            exitcode = fn()
        except KeyboardInterrupt:
            exitcode = "interrupted"
            if interrupted_banner_path is not None:
                with open(interrupted_banner_path, "ab") as f:
                    f.write(INTERRUPTED_BANNER.encode("utf-8"))
        finally:
            self.post()
        return exitcode


def clean_table(apt):
    now = time.time()
    for guid, val in apt.items():
        if now - val["last_update"] > 2 * POLL_INTERVAL:
            del apt[guid]
