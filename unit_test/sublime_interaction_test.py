'''Unit tests for interaction between the plugin code and Sublime editor'''

import postgresql_autocompletion
import unittest


class sublime_interaction(unittest.TestCase):
    '''Unit tests to test the module test1'''

    def testReturnsNothingOnNonPostgreSQLSyntax(self):
        '''The plugin returns nothing when the syntax is not PostgreSQL'''
        from sublime_mocker.view import View
        v = View({'syntax': 'something else'})
        pa = postgresql_autocompletion.postgresql_autocompletion()
        ret = pa.on_query_completions(v, None, None)
        self.assertEqual(len(ret), 0)

    def testCheckSyntax(self):
        '''CheckSyntax works'''
        from sublime_mocker import view
        v = view.View({'syntax': 'Packages/PostgreSQL Syntax Highlighting/\
PostgreSQL.tmLanguage'})
        pa = postgresql_autocompletion.postgresql_autocompletion()
        self.assertEqual(pa.checkSyntax(v), True)
        v = view.View({'syntax': 'something else'})
        self.assertEqual(pa.checkSyntax(v), False)
