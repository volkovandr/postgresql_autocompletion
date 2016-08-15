from sublime_mocker.region import Region
from sublime_mocker.settings import Settings
import os
import json

__all__ = ["view", "selection", "region", "settings"]


def load_settings(base_name):
    settings_file = os.path.dirname(os.path.abspath(__file__)) + "\\..\\" + \
        base_name
    json_file = open(settings_file)
    json_data = json.load('{"something":"nothing"}')
    print(json_data)
    json_file.close()
    return Settings(json_data)
