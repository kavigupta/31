from .test31 import Test31


class BasicTest(Test31):
    def test_success(self):
        self.assertOutput(
            ["31", "c", "echo test"],
            [
                "BEGIN SCREEN",
                "NAME = 'echo_test'",
                "test",
                "SENDING EMAIL",
                "TO = 'test@example.com'",
                "SUBJECT = 'Process succeeded in 0 seconds: echo test'",
                "BODY = 'test\\n'",
                "END SCREEN",
                "",
            ],
        )

    def test_failure(self):
        self.assertOutput(
            ["31", "c", "exit 17"],
            [
                "BEGIN SCREEN",
                "NAME = 'exit_17'",
                "SENDING EMAIL",
                "TO = 'test@example.com'",
                "SUBJECT = 'Process failed with code 17 in 0 seconds: exit 17'",
                "BODY = ''",
                "END SCREEN",
                "",
            ],
        )

    def test_multiline_output(self):
        self.assertOutput(
            ["31", "c", "echo 2; echo 3"],
            [
                "BEGIN SCREEN",
                "NAME = 'echo_2_echo_3'",
                "2",
                "3",
                "SENDING EMAIL",
                "TO = 'test@example.com'",
                "SUBJECT = 'Process succeeded in 0 seconds: echo 2; echo 3'",
                "BODY = '2\\n3\\n'",
                "END SCREEN",
                "",
            ],
        )

    def test_stdout_stderr_output(self):
        self.assertOutput(
            ["31", "c", "echo 2; python3 -c 'import sys; print(3, file=sys.stderr)'"],
            [
                "BEGIN SCREEN",
                "NAME = 'echo_2_python3_c_import_sys_print_3_file_sys.stderr'",
                "2",
                "3",
                "SENDING EMAIL",
                "TO = 'test@example.com'",
                "SUBJECT = \"Process succeeded in 0 seconds: echo 2; python3 -c 'import sys; print(3, file=sys.stderr)'\"",
                "BODY = '2\\n3\\n'",
                "END SCREEN",
                "",
            ],
        )
