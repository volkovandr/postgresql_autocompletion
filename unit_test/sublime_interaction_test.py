'''Unit tests for interaction between the plugin code and Sublime editor'''

import postgresql_autocompletion
import unittest


class sublime_interaction(unittest.TestCase):
    '''Unit tests to test the module test1'''

    def testCanLoadModule(self):
        '''Tests that the module postgresql_autocompletion can be loaded'''
        pa = postgresql_autocompletion
        self.assertIsNotNone(pa)

    def testCanLoadClass(self):
        '''Tests that the class postgresql_autocompletion can be loaded'''
        pa = postgresql_autocompletion.postgresql_autocompletion()
        self.assertIsNotNone(pa)

    def testCanImportSublimePluginMocker(self):
        '''Test the module sublime_plugin_mocker can be imported'''
        import sublime_plugin_mocker
        self.assertIsNotNone(sublime_plugin_mocker)

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
