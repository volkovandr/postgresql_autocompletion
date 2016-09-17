'''Unit tests for interaction between the plugin code and Sublime editor'''

import unittest
from postgresql_autocompletion_lib.postgresql_query_service \
    import postgresql_query_service


class postgresql_query_service_test(unittest.TestCase):
    '''Unit tests to test the module test1'''

    def testCanLoadClass(self):
        '''Can instantiate the class'''
        query_service = postgresql_query_service()
        self.assertIsNotNone(query_service)
