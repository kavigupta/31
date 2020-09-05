import os
import subprocess

import unittest

RC_TEST = os.path.join(os.path.dirname(__file__), "testrc.json")


class Test31(unittest.TestCase):
    def assertOutput(self, command, output):
        actual = subprocess.check_output([*command, "--config-file", RC_TEST])
        self.assertEqual(actual.decode("utf-8").split("\n"), output)
