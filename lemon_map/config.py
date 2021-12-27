import configparser
import logging
import os

logger = logging.getLogger(__name__)


class LemonConfig(configparser.SafeConfigParser):
    DEFAULT_CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".lemonmaprc")

    def __init__(self):
        super().__init__()
        self.file_path = None

    @classmethod
    def from_file(cls, filename=None):
        if not filename:
            filename = cls.DEFAULT_CONFIG_FILE

        if not os.path.exists(filename):
            logger.warning("file does not exist, loading default config: %s", filename)
            new_config = LemonConfig.get_default_config()
        else:
            new_config = cls()
            new_config.read(filename)
        new_config.file_path = filename
        return new_config

    @classmethod
    def get_default_config(cls):
        default_config = cls()
        default_config["DEFAULT"] = {
            "auth_file": "~/.lemon_auth.json",
        }
        return default_config

    def save_to_file(self, filename=None):
        if filename:
            destination_file = filename
        elif self.file_path:
            destination_file = self.file_path
        else:
            destination_file = self.DEFAULT_CONFIG_FILE
        with open(destination_file, "w") as c_fp:
            self.write(c_fp)
