'''Test the functionality of the sqlparser'''


import unittest
from postgresql_autocompletion_lib import sqlparser


class basic_parser_tests(unittest.TestCase):

    def testEmptyString(self):
        self.assertIsNone(sqlparser.base_parse(''))

    def testSelectList(self):
        query_text = "SELECT a, b, c FROM table"
        parsed = sqlparser.base_parse(query_text)
        self.assertEqual(parsed["select"], ("a, b, c", 8, 15))
        self.assertEqual(parsed["from"], ("table", 21, 26))
