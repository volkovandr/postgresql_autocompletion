'''The class view simulates Sublime's view object'''


import re
from sublime_mocker import region
from sublime_mocker import settings


class View():

    def __init__(
            self,
            settings_map={
                'syntax':
                    'Packages/PostgreSQL Syntax Highlighting/' + \
                    'PostgreSQL.tmLanguage'
            }
    ):
        self._settings = settings.Settings(settings_map)
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
            return self._text[position.begin():position.end()]

    def size(self):
        return len(self._text)

    def word(self, reg):
        '''Returns a modified copy of region reg such that it starts at the
        beginning of a word, and ends at the end of a word.
        Note that it may span several words.'''
        positive = ['\w', '[][!"#$%&\'()*+,./:;<=>?@\^`{|}~-]', '\s']
        negative = ['\W', '[^][!"#$%&\'()*+,./:;<=>?@\^`{|}~-]', '\S']

        search = '\W'
        beg = reg.a
        for i in range(len(positive)):
            if (
                    re.match(positive[i], self._text[beg]) or
                    beg > 0 and re.match(positive[i], self._text[beg - 1])):
                search = negative[i]
                break
        while beg > 0:
            if re.match(search, self._text[beg - 1]):
                break
            beg -= 1

        search = '\W'
        end = reg.b
        for i in range(len(positive)):
            if (
                    end < len(self._text) and
                    re.match(positive[i], self._text[end])) or \
                    re.match(positive[i], self._text[end - 1]):
                search = negative[i]
                break
        while end < len(self._text):
            if re.match(search, self._text[end]):
                break
            end += 1
        return region.Region(beg, end)
