'''Test the functionality of the sqlparser'''


import unittest
from postgresql_autocompletion_lib import sqlparser


class basic_parser_tests(unittest.TestCase):

    def testEmptyString(self):
        '''base_parse returns None on empty input'''
        self.assertIsNone(sqlparser.base_parse(''))

    def testBaseParse(self):
        '''base_parse returns positions of the main elements of the query'''
        query_text = "SELECT a, b, c FROM table"
        parsed = sqlparser.base_parse(query_text)
        self.assertEqual(parsed["select"], ("a, b, c", 8, 15))
        self.assertEqual(parsed["from"], ("table", 21, 26))

    def testCursorPositionInQuery(self):
        '''Cursor position in query wokrs'''
        parse_results = {
            "select": ("a, b, c", 8, 15),
            "from": ("table", 21, 26)}
        cursor_position_info = sqlparser.cursorPositionInQuery(
            10, parse_results)
        self.assertEqual(cursor_position_info, ("select", "a, b, c", 2))
        cursor_position_info = sqlparser.cursorPositionInQuery(
            25, parse_results)
        self.assertEqual(cursor_position_info, ("from", "table", 4))
