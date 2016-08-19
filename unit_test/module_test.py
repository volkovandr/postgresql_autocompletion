'''Unit tests for modules'''

import unittest


class import_main_modules(unittest.TestCase):
    '''Tests that the main plugin modules can be imported'''

    def testCanLoadModule(self):
        '''Tests that the module postgresql_autocompletion can be loaded'''
        import postgresql_autocompletion
        self.assertIsNotNone(postgresql_autocompletion)

    def testCanLoadClass(self):
        '''Tests that the class postgresql_autocompletion can be loaded'''
        import postgresql_autocompletion
        pa = postgresql_autocompletion.postgresql_autocompletion()
        self.assertIsNotNone(pa)


class import_mocker_modules(unittest.TestCase):
    '''Test that the mocker modules can be imported'''

    def testCanImportSublimePluginMocker(self):
        '''Test the module sublime_plugin_mocker can be imported'''
        import sublime_plugin_mocker
        self.assertIsNotNone(sublime_plugin_mocker)

    def testCanImportSublimeMocker(self):
        '''Test the module sublime_mocker can be imported'''
        import sublime_mocker
        self.assertIsNotNone(sublime_mocker)

class import_lib(unittest.TestCase):
    '''Test that the library module and classes can be loaded'''

    def testCanImportLibraryModule(self):
        import postgresql_autocompletion_lib
        self.assertIsNotNone(postgresql_autocompletion_lib)

    def testCanImportSQLParser(self):
        from postgresql_autocompletion_lib import sqlparser
        sp = sqlparser.sqlparser()
        self.assertIsNotNone(sp)