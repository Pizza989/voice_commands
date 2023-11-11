import json

from .calibration import CONFIG_PATH, calibrate


def get_config():
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)


def set_config(config):
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file)
