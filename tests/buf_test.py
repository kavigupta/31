from .test31 import Test31


class BasicTest(Test31):
    def test_success(self):
        outputs = self.get_output(
            [
                "31",
                "c",
                "-s",
                "--no-email",
                'python -u -c "import time, itertools; [(print(k), time.sleep(2)) for k in itertools.count()]"',
            ],
            check=0,
            timeout=5,
        )
        self.assertIn(outputs, [["0", "1", "2", ""], ["0", "1", ""]])
