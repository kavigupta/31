import subprocess
import re


def get_screen_program(name):
    if name == "screen":
        return _screen
    if name == "test":
        return _test
    else:
        raise RuntimeError("Only screen is currently supported as a screen_program")


def _screen(command, name):
    name = re.sub(r"[^A-Za-z0-9-., ]", "?", name)
    screen_command = ["screen", "-S", name, "-d", "-m", "--", *command]
    subprocess.check_call(screen_command)


def _test(command, name):
    print("BEGIN SCREEN")
    print(repr(name))
    subprocess.run(command)
    print("END SCREEN")
