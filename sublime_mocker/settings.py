class Settings:

    def __init__(self, settings_map):
        self._settings_map = settings_map

    def get(self, setting_name):
        if setting_name in self._settings_map:
            return self._settings_map[setting_name]
        else:
            return None
