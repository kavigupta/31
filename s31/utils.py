import subprocess
import re


def output_matches(command, regex):
    output = subprocess.run(command, shell=True, capture_output=True).stdout
    return re.match(regex, output.decode("utf-8"))
