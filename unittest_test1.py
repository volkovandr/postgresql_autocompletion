'''Unit tests for module test1'''


import unittest
import test1


class testTest1(unittest.TestCase):
    '''Unit tests to test the module test1'''

    def testAFunctionToTest(self):
        '''Tests that the function returns SomeValue'''
        self.assertEqual(
            test1.aFunctionToTest(),
            "SomeValue",
            "aFunctionToTest returns something worng")
