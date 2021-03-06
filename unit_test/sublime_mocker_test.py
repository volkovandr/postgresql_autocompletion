'''Unit tests for the sublime_mocker module'''

import unittest
import sublime_mocker as sublime
from sublime_mocker import *


class sublime_mocker(unittest.TestCase):
    '''Unit tests to test the sublime_mocker module'''

    def testCanCreateView(self):
        '''The object View of the module Sublime_mocker can be created'''
        view = sublime.view.View()
        self.assertIsNotNone(view)

    def testViewSettings(self):
        '''The view's settings can be set and read'''
        view = sublime.view.View({'a': 'a', 'b': 'b'})
        self.assertEqual(view.settings().get('a'), 'a')
        self.assertEqual(view.settings().get('b'), 'b')
        self.assertIsNone(view.settings().get('c'))

    def testViewSelection(self):
        '''View can have several Selections'''
        view = sublime.view.View()
        sel = sublime.selection.Selection(2, 3)
        view.add_selection(sel)
        view.add_selection(sublime.selection.Selection(50, 60))
        self.assertEqual(view.sel()[0].begin(), 2)
        self.assertEqual(view.sel()[0].end(), 3)
        self.assertEqual(view.sel()[1].begin(), 50)
        self.assertEqual(view.sel()[1].end(), 60)

    def testCanSetText(self):
        '''It is possible to set text of the view'''
        view = sublime.view.View()
        view.set_text("Some text")

    def testSubstrPoint(self):
        '''Can get one character from the text'''
        view = sublime.view.View()
        view.set_text("Some text")
        self.assertEqual(view.substr(0), "S")
        self.assertEqual(view.substr(1), "o")
        self.assertEqual(view.substr(2), "m")
        self.assertEqual(view.substr(3), "e")
        self.assertEqual(view.substr(4), " ")
        self.assertEqual(view.substr(5), "t")
        self.assertEqual(view.substr(8), "t")

    def testSubstrRegion(self):
        '''Can get several characters from the text'''
        view = sublime.view.View()
        view.set_text("Some text")
        self.assertEqual(view.substr(sublime.region.Region(3, 6)), "e t")
        self.assertEqual(view.substr(sublime.region.Region(0, 6)), "Some t")
        self.assertEqual(view.substr(sublime.region.Region(0, 9)), "Some text")

    def testWord(self):
        '''Can extract a word(s) from a text'''
        view = sublime.view.View()
        view.set_text("Some text about Zorro")
        reg = view.word(sublime.region.Region(3, 6))
        self.assertEqual(view.substr(reg), "Some text")
        reg = view.word(sublime.region.Region(13, 13))
        self.assertEqual(view.substr(reg), "about")
        reg = view.word(sublime.region.Region(18, 20))
        self.assertEqual(view.substr(reg), "Zorro")
        reg = view.word(sublime.region.Region(1, 1))
        self.assertEqual(view.substr(reg), "Some")
        self.assertEqual(view.word(sublime.region.Region(1, 1)).toList(),
                         sublime.region.Region(0, 4).toList())
        view.set_text("Word ;")
        self.assertEqual(view.word(sublime.region.Region(1, 5)).toList(),
                         sublime.region.Region(0, 6).toList())
        view.set_text(";;;;")
        self.assertEqual(view.word(sublime.region.Region(1, 1)).toList(),
                         sublime.region.Region(0, 4).toList())
        view.set_text("word;;;;")
        self.assertEqual(view.word(sublime.region.Region(1, 1)).toList(),
                         sublime.region.Region(0, 4).toList())
        view.set_text(";):(")
        self.assertEqual(view.word(sublime.region.Region(1, 1)).toList(),
                         sublime.region.Region(0, 4).toList())
        view.set_text(";):(word;;;;")
        self.assertEqual(view.word(sublime.region.Region(1, 1)).toList(),
                         sublime.region.Region(0, 4).toList())
        view.set_text("a  b")
        self.assertEqual(view.word(sublime.region.Region(2, 2)).toList(),
                         sublime.region.Region(1, 3).toList())
        view.set_text("a  b")
        self.assertEqual(view.word(sublime.region.Region(1, 1)).toList(),
                         sublime.region.Region(0, 1).toList())
        view.set_text("a  b")
        self.assertEqual(view.word(sublime.region.Region(3, 3)).toList(),
                         sublime.region.Region(3, 4).toList())

    def testLoadSettings(self):
        '''Test default settings'''
        settings = sublime.load_settings(
            "postgresql_autocompletion.sublime-settings")
        self.assertEqual(settings.get("postgresql_autocompletion_db_host"),
                         "localhost")

    def testRegionEquals(self):
        '''Test == operator wors for Region'''
        reg1 = sublime.region.Region(1, 1)
        reg2 = sublime.region.Region(1, 2)
        reg3 = sublime.region.Region(1, 1)
        self.assertNotEqual(reg1, reg2)
        self.assertEqual(reg1, reg3)
