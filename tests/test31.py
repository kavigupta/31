import os
import subprocess

import unittest

RC_TEST = os.path.join(os.path.dirname(__file__), "testrc.json")


class Test31(unittest.TestCase):
    def assertOutput(self, command, output, check=True):
        actual = subprocess.run(
            [*command, "--config-file", RC_TEST],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=check,
        )
        self.assertEqual(actual.stdout.decode("utf-8").split("\n"), output)
