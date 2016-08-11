'''The class view simulates Sublime's view object'''


import re
from sublime_mocker import region

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
        self._selections = []

    def settings(self):
        return self._settings

    def sel(self):
        return self._selections

    def add_selection(self, new_selection):
        self._selections.append(new_selection)

    def set_text(self, text):
        self._text = text

    def substr(self, position):
        if type(position).__name__ == "int":
            return self._text[position]
        if type(position).__name__ == "Region":
            return self._text[position.begin() - 1:position.end()]

    def size(self):
        return len(self._text)

    def word(self, reg):
        '''Returns a modified copy of region reg such that it starts at the
        beginning of a word, and ends at the end of a word.
        Note that it may span several words.'''
        beg = reg.a
        while beg > 1:
            if re.match('\W', self._text[beg-2]):
                break
            beg -= 1
        end = reg.b
        while end < len(self._text):
            if re.match('\W', self._text[end]):
                break
            end += 1
        return region.Region(beg, end)
