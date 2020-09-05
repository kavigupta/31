import attr
import sys
import subprocess


@attr.s
class Command:
    cmd_line = attr.ib()
    location = attr.ib()

    def run_teed(self, logfile):
        with open(logfile, "wb") as f:

            def write(x):
                f.write(x)
                sys.stdout.buffer.write(x)

            kwargs = dict(shell=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if self.location is not None:
                kwargs["cwd"] = self.location
            p = subprocess.Popen(self.cmd_line, **kwargs)
            while p.poll() is None:
                line = p.stdout.readline()
                if line:
                    write(line)
            return p.returncode
