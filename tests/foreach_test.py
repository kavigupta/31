import unittest

from .test31 import Test31
from s31.foreach import parse_foreach_statement, parse_foreach_statements


class TestForeachAPI(unittest.TestCase):
    def test_single_statement(self):
        self.assertEqual(
            [[("%x", "1")], [("%x", "2")], [("%x", "3")]],
            parse_foreach_statement(["%x", "1,2,3"]),
        )

    def test_zipped_statement(self):
        self.assertEqual(
            [
                [("%x", "1"), ("%y", "a")],
                [("%x", "2"), ("%y", "b")],
                [("%x", "3"), ("%y", "c")],
            ],
            parse_foreach_statement(["%x", "%y", "1,2,3", "a,b,c"]),
        )

    def test_multiple_statements(self):
        self.assertEqual(
            [
                [("%x", "1"), ("%y", "a")],
                [("%x", "1"), ("%y", "b")],
                [("%x", "2"), ("%y", "a")],
                [("%x", "2"), ("%y", "b")],
            ],
            parse_foreach_statements([["%x", "1,2"], ["%y", "a,b"]]),
        )


class TestForeachCLI(Test31):
    def test_basic_foreach(self):
        self.assertOutput(
            ["31", "c", "--no-email", "-s", "-f", "%x", "1,2,3", "echo %x"],
            ["1", "2", "3", ""],
        )

    def test_csv_foreach(self):
        self.assertOutput(
            ["31", "c", "--no-email", "-s", "-f", "%x", '",",2,3', "echo %x"],
            [",", "2", "3", ""],
        )

    def test_zip_foreach(self):
        self.assertOutput(
            [
                "31",
                "c",
                "--no-email",
                "-s",
                "-f3",
                "%x",
                "%y",
                "%z",
                "1,2,3",
                "a,b,c",
                "x,y,z",
                "echo %x %y %z",
            ],
            ["1 a x", "2 b y", "3 c z", ""],
        )

    def test_prod_foreach(self):
        self.assertOutput(
            [
                "31",
                "c",
                "--no-email",
                "-s",
                "-f",
                "%x",
                "1,2,3",
                "-f",
                "%y",
                "a,b",
                "echo %x %y",
            ],
            ["1 a", "1 b", "2 a", "2 b", "3 a", "3 b", ""],
        )

    def test_screen_foreach(self):
        self.assertOutput(
            [
                "31",
                "c",
                "--no-email",
                "-f",
                "%x",
                "1,2,3",
                "-f",
                "%y",
                "a,b",
                "echo %x %y",
            ],
            [
                "BEGIN SCREEN",
                "NAME = 'echo_1_a'",
                "1 a",
                "END SCREEN",
                "BEGIN SCREEN",
                "NAME = 'echo_1_b'",
                "1 b",
                "END SCREEN",
                "BEGIN SCREEN",
                "NAME = 'echo_2_a'",
                "2 a",
                "END SCREEN",
                "BEGIN SCREEN",
                "NAME = 'echo_2_b'",
                "2 b",
                "END SCREEN",
                "BEGIN SCREEN",
                "NAME = 'echo_3_a'",
                "3 a",
                "END SCREEN",
                "BEGIN SCREEN",
                "NAME = 'echo_3_b'",
                "3 b",
                "END SCREEN",
                "",
            ],
        )

    def test_screen_foreach_name(self):
        self.assertOutput(
            [
                "31",
                "c",
                "--no-email",
                "-f",
                "%x",
                "1,2,3",
                "-f",
                "%y",
                "a,b",
                "-n %x_%y",
                "echo %x %y",
            ],
            [
                "BEGIN SCREEN",
                "NAME = '1_a'",
                "1 a",
                "END SCREEN",
                "BEGIN SCREEN",
                "NAME = '1_b'",
                "1 b",
                "END SCREEN",
                "BEGIN SCREEN",
                "NAME = '2_a'",
                "2 a",
                "END SCREEN",
                "BEGIN SCREEN",
                "NAME = '2_b'",
                "2 b",
                "END SCREEN",
                "BEGIN SCREEN",
                "NAME = '3_a'",
                "3 a",
                "END SCREEN",
                "BEGIN SCREEN",
                "NAME = '3_b'",
                "3 b",
                "END SCREEN",
                "",
            ],
        )
