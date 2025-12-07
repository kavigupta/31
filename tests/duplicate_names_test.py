import subprocess

from .test31 import Test31, RC_TEST
from s31.main import _check_screen_name_non_overlap


class DuplicateNamesTest(Test31):
    def test_check_function_directly(self):
        """Test the duplicate check function directly"""
        commands = [
            ("echo_1", None, None),
            ("echo_1", None, None),
            ("echo_2", None, None),
        ]
        with self.assertRaises(SystemExit) as cm:
            _check_screen_name_non_overlap(commands)
        self.assertEqual(cm.exception.code, 1)
    def test_duplicate_values_in_foreach(self):
        """Test that duplicate values in foreach generate duplicate names error"""
        # Run command and capture both stdout and stderr
        result = subprocess.run(
            ["31", "c", "--no-email", "-s", "-f", "%x", "1,1,2", "echo %x", "--config-file", RC_TEST],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        # Should exit with code 1
        self.assertEqual(result.returncode, 1, f"Expected exit code 1, got {result.returncode}")
        # Should contain error message about duplicate screen names
        error_output = result.stderr
        self.assertIn("Screen names generated multiple times", error_output)
        self.assertIn("ERROR: Screen names must be unique", error_output)
        # Check that the duplicate name is listed
        self.assertIn("'echo_1'", error_output)

    def test_duplicate_after_sanitization(self):
        """Test that values that sanitize to the same name are detected as duplicates"""
        result = subprocess.run(
            ["31", "c", "--no-email", "-s", "-f", "%x", "a b,a-b", "echo %x", "--config-file", RC_TEST],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        error_output = result.stderr
        # Both "a b" and "a-b" sanitize to "a_b"
        self.assertIn("Screen names generated multiple times", error_output)
        self.assertIn("ERROR: Screen names must be unique", error_output)
        self.assertIn("'echo_a_b'", error_output)

    def test_duplicate_with_explicit_screen_name(self):
        """Test that explicit screen names that result in duplicates are detected"""
        result = subprocess.run(
            [
                "31",
                "c",
                "--no-email",
                "-s",
                "-f",
                "%x",
                "1,2",
                "-n",
                "test",
                "echo %x",
                "--config-file",
                RC_TEST,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        error_output = result.stderr
        # Both commands would have screen name "test"
        self.assertIn("Screen names generated multiple times", error_output)
        self.assertIn("ERROR: Screen names must be unique", error_output)
        self.assertIn("'test'", error_output)

    def test_duplicate_with_zipped_foreach(self):
        """Test that zipped foreach can generate duplicates"""
        result = subprocess.run(
            [
                "31",
                "c",
                "--no-email",
                "-s",
                "-f2",
                "%x",
                "%y",
                "1,1",
                "a,a",
                "echo %x %y",
                "--config-file",
                RC_TEST,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        error_output = result.stderr
        # Both combinations (1,a) would result in the same screen name
        self.assertIn("Screen names generated multiple times", error_output)
        self.assertIn("ERROR: Screen names must be unique", error_output)

    def test_multiple_duplicates(self):
        """Test that multiple duplicate names are all reported"""
        result = subprocess.run(
            ["31", "c", "--no-email", "-s", "-f", "%x", "1,1,2,2,3", "echo %x", "--config-file", RC_TEST],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        error_output = result.stderr
        # Should report both 'echo_1' and 'echo_2' as duplicates
        self.assertIn("Screen names generated multiple times", error_output)
        self.assertIn("ERROR: Screen names must be unique", error_output)
        self.assertIn("'echo_1'", error_output)
        self.assertIn("'echo_2'", error_output)

