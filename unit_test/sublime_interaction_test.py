'''Unit tests for interaction between the plugin code and Sublime editor'''

import postgresql_autocompletion
import unittest
from postgresql_autocompletion_lib.helpers import *
from sublime_mocker import view
from sublime_mocker import selection


class sublime_interaction(unittest.TestCase):
    '''Unit tests to test the module test1'''

    def testCheckSyntax(self):
        '''CheckSyntax works'''
        v = view.View({'syntax': 'Packages/PostgreSQL Syntax Highlighting' +
                       'PostgreSQL.tmLanguage'})
        self.assertEqual(checkSyntax(v), True)
        v = view.View({'syntax': 'something else'})
        self.assertEqual(checkSyntax(v), False)

    def testGetQueryText(self):
        '''getQueryText works'''
        v = view.View()
        v.set_text("This is the first query; This is the second query; " +
                   "This is the third query")
        v.add_selection(selection.Selection(8, 8))
        self.assertEqual(getQueryText(v), ("This is the first query", 8))
        v.sel()[0].a = 40
        v.sel()[0].b = 40
        self.assertEqual(getQueryText(v), ("This is the second query", 15))
        v.sel()[0].a = 70
        v.sel()[0].b = 70
        self.assertEqual(getQueryText(v), ("This is the third query", 19))
