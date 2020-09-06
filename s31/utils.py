import subprocess
import re


def output_matches(command, regex):
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout
    return re.match(regex, output.decode("utf-8"))


def format_assignments(value, assignments):
    if value is None:
        return value
    for var, val in assignments:
        value = value.replace(var, val)
    return value
