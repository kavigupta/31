import subprocess
import re


def output_matches(command, regex):
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout
    return re.match(regex, output.decode("utf-8"))
