import attr
import sys
import subprocess


from .utils import format_assignments


@attr.s
class Command:
    cmd_line = attr.ib()
    location = attr.ib()

    def run_teed(self, logfile):
        with open(logfile, "wb") as f:

            def write(x):
                f.write(x)
                sys.stdout.buffer.write(x)
                f.flush()
                sys.stdout.flush()

            p = subprocess.Popen(
                self.cmd_line,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                **self.kwargs
            )
            while p.poll() is None:
                line = p.stdout.read(1)
                if line:
                    write(line)
            while True:
                line = p.stdout.readline()
                if line:
                    write(line)
                else:
                    break
            return p.returncode

    def replace(self, assignments):
        return Command(
            cmd_line=format_assignments(self.cmd_line, assignments),
            location=format_assignments(self.location, assignments),
        )

    @property
    def kwargs(self):
        kwargs = dict(shell=1, bufsize=0)
        if self.location is not None:
            kwargs["cwd"] = self.location
        return kwargs

    def run(self):
        subprocess.run(self.cmd_line, **self.kwargs)

    def dry_run(self):
        print(self.cmd_line)
