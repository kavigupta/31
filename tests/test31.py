import os
import subprocess
import tempfile

import unittest

RC_TEST = os.path.join(os.path.dirname(__file__), "testrc.json")


class Test31(unittest.TestCase):
    def assertOutput(self, command, output, check=True, **kwargs):
        path = tempfile.mktemp()
        with open(path, "wb") as f:
            try:
                subprocess.run(
                    [*command, "--config-file", RC_TEST],
                    stdout=f,
                    stderr=subprocess.STDOUT,
                    check=check,
                    **kwargs
                )
            except subprocess.TimeoutExpired:
                pass
        with open(path) as f:
            self.assertEqual(f.read().split("\n"), output)
