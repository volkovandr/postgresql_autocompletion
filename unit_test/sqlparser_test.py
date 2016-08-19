'''Test the functionality of the sqlparser'''


import unittest
from postgresql_autocompletion_lib import sqlparser


class basic_parser_tests(unittest.TestCase):

    def testEmptyString(self):
        self.assertIsNone(sqlparser.parseSQL(''))
