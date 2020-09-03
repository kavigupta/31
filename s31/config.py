import attr
import os
import uuid
import json

from .mail import get_mail_program

CONFIG_LOC = os.path.expanduser("~/.31rc")
DEFAULT_CONFIG = dict(
    log_location=os.path.expanduser("~/.log"), mail_program="gnu_mail"
)


class Config:
    def __init__(self, config=None):
        if config is None:
            config = _load_config()
        self._config = dict(DEFAULT_CONFIG)
        self._config.update(config)
        self._mail_program = get_mail_program(self._config["mail_program"])
        if "email" not in self._config:
            raise RuntimeError(
                "You need to provide an email address, please run `31 --config email youraddress@example.com` to set this up"
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


def _load_config():
    try:
        with open(CONFIG_LOC) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def update_config(new_config):
    config = _load_config()
    config.update(new_config)
    with open(CONFIG_LOC, "w") as f:
        json.dump(config, f)
