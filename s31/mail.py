import subprocess


def get_mail_program(program_name):
    return dict(gnu_mail=_gnu_mail)[program_name]


def _gnu_mail(to, subject, body):
    subprocess.run(["mail", "-s", subject, to], input=body)
