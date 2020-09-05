from datetime import datetime
from display_timedelta import display_timedelta

FORMAT = "%Y.%m.%d.%H.%M.%S.%f"


def notify(config, command):
    start = datetime.now()
    path = datetime.strftime(start, FORMAT)
    logfile = config.create_log_file(path)

    exitcode = command.run_teed(logfile)

    end = datetime.now()

    with open(logfile, "rb") as f:
        log_contents = f.read()

    delta = end - start
    subject = "{} in {}: {}".format(
        "Process succeeded"
        if exitcode == 0
        else "Process failed with code {}".format(exitcode),
        display_timedelta(delta).replace("right now", "0 seconds"),
        command.cmd_line,
    )
    config.send_mail(subject, log_contents)
