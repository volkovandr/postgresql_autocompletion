'''Unit tests for PostgreSQL abstraction interface class
called postgresql_query_service
If you want to run the tests you need to create an empty database here:
host: localhost
port: 5432
database: test_database
username: test_user
password: test_password

The testing code will recreate the schema test_schema in the database
and create all necessary objects there.
'''

import unittest
from postgresql_query_service.postgresql_query_service \
    import postgresql_query_service


class postgresql_query_service_test(unittest.TestCase):
    '''Unit tests for postgresql_query_service
    In order to make the tests work you should have a PostgreSQL server
    running on localhost and create a user 'test_user' with password
    'test_password' being able to connect and create objects in a database
    'test_database'
    '''

    def testCanLoadClass(self):
        '''Can instantiate the class'''
        query_service = postgresql_query_service()
        self.assertIsNotNone(query_service)

    def testDBConnect(self):
        query_service = postgresql_query_service()
        query_service.connect(
            host='localhost',
            port='5432',
            database='test_database',
            user='test_user',
            password='test_password')

    def createTestSchema(self):
        query_service = postgresql_query_service()
        query_service.connect(
            host='localhost',
            port='5432',
            database='test_database',
            user='test_user',
            password='test_password')
        query_service.connection.execute('''
            DROP SCHEMA IF EXISTS test_schema CASCADE;
            DROP SCHEMA IF EXISTS test_schema2 CASCADE;
            DROP TABLE IF EXISTS test1_public;
            DROP TABLE IF EXISTS test2_public;
            CREATE SCHEMA test_schema;
            CREATE SCHEMA test_schema2;
            CREATE TABLE test1_public(a int);
            CREATE TABLE test2_public(a int);
            CREATE TABLE test_schema.table1_test1(a int);
            CREATE TABLE test_schema.table2_test1(a int);
            ''')

    def testGetSchemas(self):
        self.createTestSchema()
        query_service = postgresql_query_service()
        query_service.connect(
            host='localhost',
            port='5432',
            database='test_database',
            user='test_user',
            password='test_password')
        schemas = query_service.getSchemas()
        self.assertEqual([
            'information_schema',
            'pg_catalog',
            'public',
            'test_schema',
            'test_schema2'], schemas)

    def testIsConnected(self):
        query_service = postgresql_query_service()
        query_service.connect(
            host='localhost',
            port='5432',
            database='test_database',
            user='test_user',
            password='test_password')
        self.assertTrue(query_service.isConnected())

    def testGetTablesPublic(self):
        '''Returns tables from public when the schemaname not given'''
        self.createTestSchema()
        query_service = postgresql_query_service()
        query_service.connect(
            host='localhost',
            port='5432',
            database='test_database',
            user='test_user',
            password='test_password')
        tables = query_service.getTables()
        self.assertEqual(
            tables,
            [
                ("test1_public", "public"),
                ("test2_public", "public")])

    def testGetTablesTestSchema(self):
        '''Returns tables from public when the schemaname not given'''
        self.createTestSchema()
        query_service = postgresql_query_service()
        query_service.connect(
            host='localhost',
            port='5432',
            database='test_database',
            user='test_user',
            password='test_password')
        tables = query_service.getTables("test_schema")
        self.assertEqual(
            tables,
            [
                ("table1_test1", "test_schema"),
                ("table2_test1", "test_schema")])
