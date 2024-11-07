import configparser
from functools import cache

@cache
def get_config():
    config = configparser.ConfigParser()
    config.read("./config/development.cfg")
    return config
