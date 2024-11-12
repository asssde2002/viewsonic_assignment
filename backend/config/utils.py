import configparser
import os
from functools import cache


@cache
def get_config():
    config = configparser.ConfigParser()
    path = os.path.dirname(os.path.abspath(__file__))
    config.read(f"{path}/development.cfg")
    return config
