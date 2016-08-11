'''Unit tests for the general functionality of the plubin'''

import postgresql_autocompletion
import unittest


class genral_functionality(unittest.TestCase):
    '''Unit tests to test the module test1'''

    def testReturnsNothingOnNonPostgreSQLSyntax(self):
        '''The plugin returns nothing when the syntax is not PostgreSQL'''
        from sublime_mocker.view import View
        v = View({'syntax': 'something else'})
        pa = postgresql_autocompletion.postgresql_autocompletion()
        ret = pa.on_query_completions(v, None, None)
        self.assertEqual(len(ret), 0)
