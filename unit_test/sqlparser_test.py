'''Test the functionality of the sqlparser'''


import unittest
from postgresql_autocompletion_lib import sqlparser


class basic_parser_tests(unittest.TestCase):

    def testEmptyString(self):
        self.assertIsNone(sqlparser.parseSQL(''))

    def testSelectList(self):
        query_text = "SELECT a, b, c FROM table"
        parsed = sqlparser.parseSQL(query_text)
        self.assertEqual(parsed["Select-List"],("a, b, c", 8, 14))
