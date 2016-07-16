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
