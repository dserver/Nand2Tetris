import unittest
from Code import Code

class codetests(unittest.TestCase):
    def testValueFunction(self):
        c = Code()
        self.assertEqual("0b0000000000000000", c.value(0))
        self.assertEqual("0b0000000000000010", c.value(2))