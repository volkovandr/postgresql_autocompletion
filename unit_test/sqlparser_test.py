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
        self.assertEqual(parsed["select"], ("a, b, c", 7, 14))
        self.assertEqual(parsed["from"], ("table", 20, 25))

    def testParseFrom(self):
        '''parseFrom works'''
        test_cases = [
            ("", []),
            ("table1", [{"schema_or_table_name": ("table1", 0, 6)}]),
            ("table1 as t1", [{"table_name": ("table1", 0, 6),
                               "alias": ("t1", 10, 12)}]),
            ("table1 t1", [{"table_name": ("table1", 0, 6),
                            "alias": ("t1", 7, 9)}]),
            ("schema_1.table1 as t1", [{"schema_name": ("schema_1", 0, 8),
                                        "table_name": ("table1", 9, 15),
                                        "alias": ("t1", 19, 21)}]),
            ("schema1.table1 t1", [{"schema_name": ("schema1", 0, 7),
                                    "table_name": ("table1", 8, 14),
                                    "alias": ("t1", 15, 17)}]),
            ("schema1.table1", [{"schema_name": ("schema1", 0, 7),
                                 "table_name": ("table1", 8, 14)}]),
            ("table1, table2", [
                {"schema_or_table_name": ("table1", 0, 6)},
                {"schema_or_table_name": ("table2", 8, 14)}]),
            ("table1 as t1, table2 as t2", [
                {"table_name": ("table1", 0, 6), "alias": ("t1", 10, 12)},
                {"table_name": ("table2", 14, 20), "alias": ("t2", 24, 26)}]),
            ("table1, schema2.table2 t2", [
                {"schema_or_table_name": ("table1", 0, 6)},
                {
                    "schema_name": ("schema2", 8, 15),
                    "table_name": ("table2", 16, 22),
                    "alias": ("t2", 23, 25)}]),
            ("schema1.table1 t1, schema2.table2 as t2", [
                {
                    "schema_name": ("schema1", 0, 7),
                    "table_name": ("table1", 8, 14),
                    "alias": ("t1", 15, 17)},
                {
                    "schema_name": ("schema2", 19, 26),
                    "table_name": ("table2", 27, 33),
                    "alias": ("t2", 37, 39)}]),
            ("s1.t1, s2.t2, s3.t3, s4.t4", [
                {"schema_name": ("s1", 0, 2), "table_name": ("t1", 3, 5)},
                {"schema_name": ("s2", 7, 9), "table_name": ("t2", 10, 12)},
                {"schema_name": ("s3", 14, 16), "table_name": ("t3", 17, 19)},
                {"schema_name": ("s4", 21, 23), "table_name": ("t4", 24, 26)}]),
            ("bla1 bla2 bla3 bla4", []),
            ('''schema1.table1
            as zorro  ,
            schema2.table2
            mumba''', [
                {
                    "schema_name": ("schema1", 0, 7),
                    "table_name": ("table1", 8, 14),
                    "alias": ("zorro", 30, 35)},
                {
                    "schema_name": ("schema2", 51, 58),
                    "table_name": ("table2", 59, 65),
                    "alias": ("mumba", 78, 83)}]),
            ("bla.bla, zok.mok, a b c, kum.zum", [
                {
                    "schema_name": ("bla", 0, 3),
                    "table_name": ("bla", 4, 7)},
                {
                    "schema_name": ("zok", 9, 12),
                    "table_name": ("mok", 13, 16)},
                {
                    "schema_name": ("kum", 25, 28),
                    "table_name": ("zum", 29, 32)}]),
            ("test_schema.", [
                {
                    "schema_name": ("test_schema", 0, 11),
                    "table_name": ("", 12, 12)}])]
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

    def testCursorPositionInQueryOut(self):
        '''CursorPositionInQuery returns None when cursor is not in any element'''
        parse_results = {
            "select": ("a, b, c", 8, 15),
            "from": ("table", 21, 26)}
        cursor_position_info = sqlparser.cursorPositionInQuery(
            100, parse_results)
        self.assertIsNone(cursor_position_info)

