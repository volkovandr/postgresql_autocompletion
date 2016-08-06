'''Unit tests for the sublime_mocker module'''

import unittest
import sublime_mocker as sublime
from sublime_mocker import *

class sublime_interaction(unittest.TestCase):
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

