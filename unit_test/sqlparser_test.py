'''Test the functionality of the sqlparser'''


import unittest
from postgresql_autocompletion_lib import sqlparser


class basic_parser_tests(unittest.TestCase):

    def testEmptyString(self):
        '''base_parse returns empty on empty input'''
        self.assertIsNone(sqlparser.base_parse(''))

    def testBaseParse(self):
        '''base_parse returns positions of the main elements of the query'''
        query_text = "SELECT a, b, c FROM table"
        parsed = sqlparser.base_parse(query_text)
        self.assertEqual(parsed["select"], ("a, b, c", 8, 15))
        self.assertEqual(parsed["from"], ("table", 21, 26))

    def testParseFrom(self):
        '''parseFrom works'''
        test_cases = [
            ("", []),
            ("table1", [{"schema_or_table_name": ("table1", 1, 7)}]),
            ("table1 as t1", [{"table_name": ("table1", 1, 7),
                               "alias": ("t1", 11, 13)}]),
            ("table1 t1", [{"table_name": ("table1", 1, 7),
                            "alias": ("t1", 8, 10)}]),
            ("schema1.table1 as t1", [{"schema_name": ("schema1", 1, 8),
                                       "table_name": ("table1", 9, 15),
                                       "alias": ("t1", 19, 21)}]),
            ("schema1.table1 t1", [{"schema_name": ("schema1", 1, 8),
                                    "table_name": ("table1", 9, 15),
                                    "alias": ("t1", 16, 18)}]),
            ("schema1.table1", [{"schema_name": ("schema1", 1, 8),
                                 "table_name": ("table1", 9, 15)}]),
            ("table1, table2", [
                {"schema_or_table_name": ("table1", 1, 7)},
                {"schema_or_table_name": ("table2", 9, 15)}]),
            ("table1 as t1, table2 as t2", [
                {"table_name": ("table1", 1, 7), "alias": ("t1", 11, 13)},
                {"table_name": ("table2", 15, 21), "alias": ("t2", 25, 27)}]),
            ("table1, schema2.table2 t2", [
                {"schema_or_table_name": ("table1", 1, 7)},
                {
                    "schema_name": ("schema2", 9, 16),
                    "table_name": ("table2", 17, 23),
                    "alias": ("t2", 24, 26)}]),
            ("schema1.table1 t1, schema2.table2 as t2", [
                {
                    "schema_name": ("schema1", 1, 8),
                    "table_name": ("table1", 9, 15),
                    "alias": ("t1", 16, 18)},
                {
                    "schema_name": ("schema2", 20, 27),
                    "table_name": ("table2", 28, 34),
                    "alias": ("t2", 38, 40)}]),
            ("s1.t1, s2.t2, s3.t3, s4.t4", [
                {"schema_name": ("s1", 1, 3), "table_name": ("t1", 4, 6)},
                {"schema_name": ("s2", 8, 10), "table_name": ("t2", 11, 13)},
                {"schema_name": ("s3", 15, 17), "table_name": ("t3", 18, 20)},
                {"schema_name": ("s4", 22, 24), "table_name": ("t4", 25, 27)}]),
            ("bla1 bla2 bla3 bla4", []),
            ('''schema1.table1
            as zorro  ,
            schema2.table2
            mumba''', [
                {
                    "schema_name": ("schema1", 1, 8),
                    "table_name": ("table1", 9, 15),
                    "alias": ("zorro", 31, 36)},
                {
                    "schema_name": ("schema2", 52, 59),
                    "table_name": ("table2", 60, 66),
                    "alias": ("mumba", 79, 84)}]),
            ("bla.bla, zok.mok, a b c, kum.zum", [
                {
                    "schema_name": ("bla", 1, 4),
                    "table_name": ("bla", 5, 8)},
                {
                    "schema_name": ("zok", 10, 13),
                    "table_name": ("mok", 14, 17)},
                {
                    "schema_name": ("kum", 26, 29),
                    "table_name": ("zum", 30, 33)}])]
        for test_case in test_cases:
            from_clause_text = test_case[0]
            from_clause_parsed = sqlparser.parseFrom(from_clause_text)
            self.assertEqual(test_case[1], from_clause_parsed)


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
