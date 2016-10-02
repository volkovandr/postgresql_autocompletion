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

    def testCursorAtSchemaName(self):
        '''Returns schema names when cursor stands in the name of a schema'''
        v = View()
        v.set_text("SELECT a, b, c FROM tes.table1")
        v.add_selection(Selection(24, 24))
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

    def testConnectsToDatabase(self):
        '''The plugin does connect to the database'''
        v = View()
        v.set_text("SELECT a, b, c FROM test_schema.table1")
        v.add_selection(Selection(24, 24))
        query_service = dbmocker_query_service()
        pa = postgresql_autocompletion(query_service)
        pa.on_query_completions(v, "tes", None)
        self.assertTrue(query_service.isConnected())
