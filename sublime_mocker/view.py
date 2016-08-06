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

    class Selection():
        '''Represents Sublimes Selection class'''
        a = 0
        b = 0

        def __init__(self, a=0, b=0):
            self.a = a
            self.b = b

        def begin(self):
            if self.a < self.b:
                return self.a
            else:
                return self.b

        def end(self):
            if self.b > self.a:
                return self.b
            else:
                return self.a

    _selections = []

    def sel(self):
        return self._selections

    def add_selection(self, new_selection):
        self._selections.append(new_selection)
