from .test31 import Test31


class BasicTest(Test31):
    def test_success(self):
        self.assertOutput(
            [
                "31",
                "c",
                "-s",
                "--no-email",
                'python -u -c "import time, itertools; [(print(k), time.sleep(2)) for k in itertools.count()]"',
            ],
            [
                "0",
                "1",
                "2",
                "",
            ],
            check=0,
            timeout=5,
        )
