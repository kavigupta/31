from datetime import datetime
from display_timedelta import display_timedelta
import sys

from . import utils

FORMAT = "%Y.%m.%d.%H.%M.%S.%f"


def notify(config, command):
    start = datetime.now()
    path = datetime.strftime(start, FORMAT)
    logfile = config.create_log_file(path)

    with open(logfile, "wb") as f:
        exitcode = utils.run_with_tee(command, (f, sys.stdout.buffer))

    end = datetime.now()

    with open(logfile, "rb") as f:
        log_contents = f.read()

    delta = end - start
    subject = "{} in {}: {}".format(
        "Process succeeded"
        if exitcode == 0
        else "Process failed with {}".format(exitcode),
        display_timedelta(delta),
        command,
    )
    config.send_mail(subject, log_contents)
