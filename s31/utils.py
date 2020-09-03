import subprocess
import re


def run_with_tee(command, output_bytestreams):
    p = subprocess.Popen(
        command, shell=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    while p.poll() is None:
        line = p.stdout.readline()
        if line:
            for stream in output_bytestreams:
                stream.write(line)
    return p.returncode


def output_matches(command, regex):
    output = subprocess.run(command, shell=True, capture_output=True).stdout
    return re.match(regex, output.decode("utf-8"))
