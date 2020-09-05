import subprocess
import sys

from .utils import output_matches


def get_mail_program(program_name):
    if program_name == "detect":
        if output_matches("mail -V", "^mail \(GNU Mailutils\).*"):
            program_name = "gnu_mail"
        elif output_matches("mutt -h", "Mutt .*"):
            program_name = "mutt"
        else:
            raise RuntimeError(
                "Could not detect a mail program. Please see the documentation for a list of supported programs."
            )
    return dict(gnu_mail=_gnu_mail, mutt=_mutt, test=_test)[program_name]


def _gnu_mail(to, subject, body):
    subprocess.run(["mail", "-s", subject, to], input=body)


def _mutt(to, subject, body):
    subprocess.run(["mutt", "-s", subject, to], input=body)


def _test(to, subject, body):
    print("SENDING EMAIL")
    print("TO =", repr(to))
    print("SUBJECT =", repr(subject))
    print("BODY =", repr(body.decode("utf-8")))
    sys.stdout.flush()
