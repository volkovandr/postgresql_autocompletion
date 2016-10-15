'''Unit tests for the general functionality of the plubin'''

from postgresql_autocompletion import postgresql_autocompletion
from sublime_mocker.view import View
from sublime_mocker.selection import Selection
from query_service_mocker.dbmocker_query_service import dbmocker_query_service
import unittest


class genral_functionality(unittest.TestCase):

    def testReturnsNothingOnNonPostgreSQLSyntax(self):
        '''The plugin returns nothing when the syntax is not PostgreSQL'''
        v = View({'syntax': 'something else'})
        pa = postgresql_autocompletion()
        ret = pa.on_query_completions(v, None, None)
        self.assertEqual(len(ret), 0)

    def testConnectsToDatabase(self):
        '''The plugin does connect to the database'''
        v = View()
        v.set_text("SELECT a, b, c FROM test_schema.table1")
        v.add_selection(Selection(24, 24))
        query_service = dbmocker_query_service()
        pa = postgresql_autocompletion(query_service)
        pa.on_query_completions(v, "tes", None)
        self.assertTrue(query_service.isConnected())


class corner_cases(unittest.TestCase):

    def testEmptyFromList(self):
        '''The plugin returns tables and schemas when the cursor is just after
        the keyword FROM '''
        v = View()
        v.set_text("SELECT a, b, c FROM ")
        v.add_selection(Selection(20, 20))
        pa = postgresql_autocompletion(dbmocker_query_service())
        ret = pa.on_query_completions(v, "", None)
        self.assertEqual(
            ret,
            [
                ["information_schema\tschema", "information_schema."],
                ["pg_catalog\tschema", "pg_catalog."],
                ["public\tschema", "public."],
                ["test_schema\tschema", "test_schema."],
                ["test_schema2\tschema", "test_schema2."],
                ["test1_public\ttable in public", "test1_public"],
                ["test2_public\ttable in public", "test2_public"]])

    def testCursorBeforeSemicolon(self):
        '''Plugin works when the cursor is just before semicolon'''
        v = View()
        v.set_text("SELECT a, b, c FROM ;")
        v.add_selection(Selection(20, 20))
        pa = postgresql_autocompletion(dbmocker_query_service())
        ret = pa.on_query_completions(v, "", None)
        self.assertEqual(
            ret,
            [
                ["information_schema\tschema", "information_schema."],
                ["pg_catalog\tschema", "pg_catalog."],
                ["public\tschema", "public."],
                ["test_schema\tschema", "test_schema."],
                ["test_schema2\tschema", "test_schema2."],
                ["test1_public\ttable in public", "test1_public"],
                ["test2_public\ttable in public", "test2_public"]])

    def testCursorBeforeSemicolonMultipleTables(self):
        '''Plugin works when the cursor is just before semicolon'''
        print('***************************')
        v = View()
        v.set_text("SELECT a, b, c FROM schema.table, ;")
        v.add_selection(Selection(34, 34))
        pa = postgresql_autocompletion(dbmocker_query_service())
        ret = pa.on_query_completions(v, "", None)
        self.assertEqual(
            ret,
            [
                ["information_schema\tschema", "information_schema."],
                ["pg_catalog\tschema", "pg_catalog."],
                ["public\tschema", "public."],
                ["test_schema\tschema", "test_schema."],
                ["test_schema2\tschema", "test_schema2."],
                ["test1_public\ttable in public", "test1_public"],
                ["test2_public\ttable in public", "test2_public"]])

    def testNotAQuery(self):
        '''Plugin returns nothing when this is not a query at all'''
        v = View()
        v.set_text("This is not a query;")
        v.add_selection(Selection(10, 10))
        pa = postgresql_autocompletion(dbmocker_query_service())
        ret = pa.on_query_completions(v, "", None)
        self.assertEqual(
            ret,
            [])


class test_from_autocompletion(unittest.TestCase):

    def testCursorAtSchemaName(self):
        '''Returns schema names when cursor stands in the name of a schema'''
        v = View()
        v.set_text("SELECT a, b, c FROM tes.table1")
        v.add_selection(Selection(23, 23))
        pa = postgresql_autocompletion(dbmocker_query_service())
        ret = pa.on_query_completions(v, "tes", None)
        self.assertEqual(
            ret,
            [
                ["information_schema\tschema", "information_schema"],
                ["pg_catalog\tschema", "pg_catalog"],
                ["public\tschema", "public"],
                ["test_schema\tschema", "test_schema"],
                ["test_schema2\tschema", "test_schema2"]])

    def testCursorAtSchemaOrTableName(self):
        '''Returns schema and table names when cursor stands at a place
        where it is not clear if that is a schema or table name'''
        v = View()
        v.set_text("SELECT a, b, c FROM tes")
        v.add_selection(Selection(23, 23))
        pa = postgresql_autocompletion(dbmocker_query_service())
        ret = pa.on_query_completions(v, "tes", None)
        self.assertEqual(
            ret,
            [
                ["information_schema\tschema", "information_schema."],
                ["pg_catalog\tschema", "pg_catalog."],
                ["public\tschema", "public."],
                ["test_schema\tschema", "test_schema."],
                ["test_schema2\tschema", "test_schema2."],
                ["test1_public\ttable in public", "test1_public"],
                ["test2_public\ttable in public", "test2_public"]])

    def testCursorAtTableName(self):
        '''Returns name of the tables when cursor is in the table name'''
        v = View()
        v.set_text("SELECT a, b, c FROM test_schema.t")
        v.add_selection(Selection(33, 33))
        pa = postgresql_autocompletion(dbmocker_query_service())
        ret = pa.on_query_completions(v, "t", None)
        self.assertEqual(
            ret,
            [
                ["table1_test1\ttable in test_schema", "table1_test1"],
                ["table2_test1\ttable in test_schema", "table2_test1"]])

    def testMultipleTables(self):
        '''Returns schema or table names when cursor is just after the comma'''
        v = View()
        v.set_text("SELECT a, b, c FROM public.table1, ")
        v.add_selection(Selection(35, 35))
        pa = postgresql_autocompletion(dbmocker_query_service())
        ret = pa.on_query_completions(v, "", None)
        self.assertEqual(
            ret,
            [
                ["information_schema\tschema", "information_schema."],
                ["pg_catalog\tschema", "pg_catalog."],
                ["public\tschema", "public."],
                ["test_schema\tschema", "test_schema."],
                ["test_schema2\tschema", "test_schema2."],
                ["test1_public\ttable in public", "test1_public"],
                ["test2_public\ttable in public", "test2_public"]])
