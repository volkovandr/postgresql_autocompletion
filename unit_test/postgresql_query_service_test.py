'''Unit tests for interaction between the plugin code and Sublime editor'''

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
