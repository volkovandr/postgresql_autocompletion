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

    def testCanImportSublimeMocker(self):
        '''Test the module sublime_mocker can be imported'''
        import sublime_mocker
        self.assertIsNotNone(sublime_mocker)

    def testCanImportSublimePluginMocker(self):
        '''Test the module sublime_plugin_mocker can be imported'''
        import sublime_plugin_mocker
        self.assertIsNotNone(sublime_plugin_mocker)

#    def testReturnsNothingOnNonPostgreSQLSyntax(self):
#        '''The plugin returns nothing when the file being edited
#        has other syntax than PostgreSQL'''
#        raise Exception("Not implemented")
