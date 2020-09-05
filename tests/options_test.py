from .test31 import Test31
import os


class TestOptions(Test31):
    def test_sync(self):
        self.assertOutput(
            ["31", "c", "--sync", "echo test"],
            [
                "test",
                "SENDING EMAIL",
                "TO = 'test@example.com'",
                "SUBJECT = 'Process succeeded in 0 seconds: echo test'",
                "BODY = 'test\\n'",
                "",
            ],
        )

    def test_name(self):
        self.assertOutput(
            ["31", "c", "-n", "testing command", "echo test"],
            [
                "BEGIN SCREEN",
                "NAME = 'testing_command'",
                "test",
                "SENDING EMAIL",
                "TO = 'test@example.com'",
                "SUBJECT = 'Process succeeded in 0 seconds: echo test'",
                "BODY = 'test\\n'",
                "END SCREEN",
                "",
            ],
        )

    def test_no_emails(self):
        self.assertOutput(
            ["31", "c", "--no-email", "echo test"],
            [
                "BEGIN SCREEN",
                "NAME = 'echo_test'",
                "test",
                "END SCREEN",
                "",
            ],
        )

    def test_pwd(self):
        self.assertOutput(
            [
                "31",
                "c",
                "-l",
                "..",
                "-n",
                "testing command",
                "python -c 'import os; print(os.getcwd())'",
            ],
            [
                "BEGIN SCREEN",
                "NAME = 'testing_command'",
                os.path.abspath(".."),
                "SENDING EMAIL",
                "TO = 'test@example.com'",
                "SUBJECT = \"Process succeeded in 0 seconds: python -c 'import os; print(os.getcwd())'\"",
                "BODY = '{}\\n'".format(os.path.abspath("..")),
                "END SCREEN",
                "",
            ],
        )
