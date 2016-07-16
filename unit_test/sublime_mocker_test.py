'''Unit tests for the sublime_mocker module'''

import unittest
import sublime_mocker as sublime


class sublime_interaction(unittest.TestCase):
    '''Unit tests to test the sublime_mocker module'''

    def testCanImportSublimeMocker(self):
        '''Test the module sublime_mocker can be imported'''
        import sublime_mocker
        self.assertIsNotNone(sublime_mocker)

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
