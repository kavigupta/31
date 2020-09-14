import subprocess
import re

import shelve
from filelock import FileLock


def output_matches(command, regex):
    output = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout
    return re.match(regex, output.decode("utf-8"))


def format_assignments(value, assignments):
    if value is None:
        return value
    for var, val in assignments:
        value = value.replace(var, val)
    return value


def sanitize(name):
    return re.sub("[^A-Za-z0-9_.]+", "_", name).strip("_")


def set_key(file, key):
    with FileLock(file + ".lock"):
        with shelve.open(file + ".shelve") as s:
            s[key] = True


def get_keys(file):
    with FileLock(file + ".lock"):
        with shelve.open(file + ".shelve") as s:
            return {k for k in s if s[k]}
