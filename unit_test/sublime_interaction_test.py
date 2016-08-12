'''Unit tests for interaction between the plugin code and Sublime editor'''

import postgresql_autocompletion
import unittest
from sublime_mocker import view
from sublime_mocker import selection


class sublime_interaction(unittest.TestCase):
    '''Unit tests to test the module test1'''

    def testCheckSyntax(self):
        '''CheckSyntax works'''
        v = view.View({'syntax': 'Packages/PostgreSQL Syntax Highlighting' +
                       'PostgreSQL.tmLanguage'})
        pa = postgresql_autocompletion.postgresql_autocompletion()
        self.assertEqual(pa.checkSyntax(v), True)
        v = view.View({'syntax': 'something else'})
        self.assertEqual(pa.checkSyntax(v), False)

    def testGetQueryText(self):
        '''getQueryText works'''
        v = view.View()
        v.set_text("This is the first query; This is the second query; " +
                   "This is the third query")
        v.add_selection(selection.Selection(8, 8))
        pa = postgresql_autocompletion.postgresql_autocompletion()
        self.assertEqual(pa.getQueryText(v), "This is the first query")
