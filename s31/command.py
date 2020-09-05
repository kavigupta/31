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

            p = subprocess.Popen(
                self.cmd_line,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                **self.kwargs
            )
            while p.poll() is None:
                line = p.stdout.readline()
                if line:
                    write(line)
            while True:
                line = p.stdout.readline()
                if line:
                    write(line)
                else:
                    break
            return p.returncode

    @property
    def kwargs(self):
        kwargs = dict(shell=1)
        if self.location is not None:
            kwargs["cwd"] = self.location
        return kwargs

    def run(self):
        subprocess.run(self.cmd_line, **self.kwargs)
