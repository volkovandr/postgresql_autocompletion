'''Unit tests for interaction between the plugin code and Sublime editor'''

import unittest
from query_service_mocker.dbmocker_query_service \
    import dbmocker_query_service


class dbmocker(unittest.TestCase):

    def testCanLoadClass(self):
        '''Can instantiate the class'''
        dbmocker = dbmocker_query_service()
        self.assertIsNotNone(dbmocker)

    def testCanConnect(self):
        '''Can connect to the database'''
        dbmocker = dbmocker_query_service()
        dbmocker.connect("host", "port", "database", "user", "password")
        self.assertEqual(True, dbmocker.isConnected())

    def testGetSchemas(self):
        '''getSchemas returns the test schemas'''
        dbmocker = dbmocker_query_service()
        dbmocker.connect("host", "port", "database", "user", "password")
        schemas = dbmocker.getSchemas()
        self.assertEqual(
            schemas,
            [
                "information_schema",
                "pg_catalog",
                "public",
                "test_schema",
                "test_schema2"])

    def testGetTablesPublic(self):
        '''getTables returns the tables from public schema
        if the schema is not set'''
        dbmocker = dbmocker_query_service()
        dbmocker.connect("host", "port", "database", "user", "password")
        tables = dbmocker.getTables()
        self.assertEqual(
            tables,
            [
                ("test1_public", "public"),
                ("test2_public", "public")])

    def testGetTablesTestSchema(self):
        '''getTables returns the tables from test schema
        if the schema is not set'''
        dbmocker = dbmocker_query_service()
        dbmocker.connect("host", "port", "database", "user", "password")
        tables = dbmocker.getTables('test_schema')
        self.assertEqual(
            tables,
            [
                ("table1_test1", "test_schema"),
                ("table2_test1", "test_schema")])
