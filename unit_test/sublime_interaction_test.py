'''Unit tests for interaction between the plugin code and Sublime editor'''

import postgresql_autocompletion
import unittest
from postgresql_autocompletion_lib.helpers import *
from sublime_mocker import view
from sublime_mocker import selection


class sublime_interaction(unittest.TestCase):

    def testCheckSyntax(self):
        '''CheckSyntax works'''
        v = view.View({'syntax': 'Packages/PostgreSQL Syntax Highlighting' +
                       'PostgreSQL.tmLanguage'})
        self.assertEqual(checkSyntax(v, "PostgreSQL"), True)
        v = view.View({'syntax': 'something else'})
        self.assertEqual(checkSyntax(v, "PostgreSQL"), False)

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

    def testGetSettings(self):
        '''getSettings works'''
        default_settings = {
            "postgresql_autocompletion_db_host": "localhost",
            "postgresql_autocompletion_db_port": "5432",
            "postgresql_autocompletion_db_name": "test",
            "postgresql_autocompletion_db_user": "test",
            "postgresql_autocompletion_db_password": "password",
            "postgresql_autocompletion_syntax": "PostgreSQL"}
        v = view.View()
        settings = getSettings(v)
        self.assertEqual(settings, default_settings)
