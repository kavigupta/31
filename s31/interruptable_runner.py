import time
import uuid

from .active_process_table import active_process_table


INTERRUPTED_BANNER = """
=======================================
INTERRUPTED BY USER
=======================================
"""


class InterruptableRunner:
    def __init__(self, name, pid, cmd_to_use):
        self.name = name
        self.pid = pid
        self.cmd_to_use = cmd_to_use
        self.guid = str(uuid.uuid4())
        self.timestamp = time.time()

    def pre(self):
        with active_process_table() as t:
            t[self.guid] = dict(
                name=self.name,
                pid=self.pid,
                cmd=self.cmd_to_use.cmd_line,
                timestamp=self.timestamp,
            )

    def post(self):
        with active_process_table() as t:
            del t[self.guid]

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
