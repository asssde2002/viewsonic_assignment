import configparser
from functools import cache

@cache
def get_config():
    config = configparser.ConfigParser()
    config.read("./development.cfg")
    return config