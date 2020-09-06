import os
import re
import json

from .mail import get_mail_program
from .screen import get_screen_program

DEFAULT_CONFIG = dict(
    log_location=os.path.expanduser("~/.log"),
    mail_program="detect",
    screen_program="screen",
)


class Config:
    def __init__(self, config_file):
        config = _load_config(config_file)
        self._config = dict(DEFAULT_CONFIG)
        self._config.update(config)
        self._mail_program = get_mail_program(self._config["mail_program"])
        self._screen_program = get_screen_program(self._config["screen_program"])
        if "email" not in self._config:
            raise RuntimeError(
                "You need to provide an email address, please run `31 config email youraddress@example.com` to set this up"
            )
        self._email = self._config["email"]

    def create_log_file(self, path):
        ll = self._config["log_location"]
        try:
            os.makedirs(ll)
        except FileExistsError:
            pass
        return os.path.join(ll, path)

    def send_mail(self, subject, body):
        return self._mail_program(to=self._email, subject=subject, body=body)

    def launch_screen(self, command, name):
        return self._screen_program(command=command, name=name)


def _load_config(config_file):
    try:
        with open(config_file) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def update_config(config_file, new_config):
    config = _load_config(config_file)
    config.update(new_config)
    with open(config_file, "w") as f:
        json.dump(config, f)
