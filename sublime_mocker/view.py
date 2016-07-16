'''The class view simulates Sublime's view object'''


class View():
    class Settings():

        def __init__(self, settings_map):
            self.settings = settings_map

        def get(self, setting_name):
            if setting_name in self.settings:
                return self.settings[setting_name]
            else:
                return None
        pass

    def __init__(
            self,
            settings_map={
                'syntax':
                    'Packages/PostgreSQL Syntax Highlighting/\
                    PostgreSQL.tmLanguage'
            }
    ):
        self._settings = View.Settings(settings_map)

    def settings(self):
        return self._settings
