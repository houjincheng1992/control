import os
import ConfigParser

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

CONF_PATH = os.path.join(BASE_PATH, "config")


def setup_config(config_file=os.path.join(CONF_PATH, "config.ini")):
    config_file = os.getenv("CONFIG_FILE", config_file)
    config = ConfigParser.SafeConfigParser()
    config.read(config_file)
    return config
