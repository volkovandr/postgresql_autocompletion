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
                "public",
                "test_schema",
                "pg_catalog",
                "information_schema"].sort())
