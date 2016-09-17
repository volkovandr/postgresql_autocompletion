'''Unit tests for interaction between the plugin code and Sublime editor'''

import unittest
from query_service_mocker.dbmocker_query_service \
    import dbmocker_query_service


class dbmocker(unittest.TestCase):
    '''Unit tests to test the module test1'''

    def testCanLoadClass(self):
        '''Can instantiate the class'''
        dbmocker = dbmocker_query_service()
        self.assertIsNotNone(dbmocker)
