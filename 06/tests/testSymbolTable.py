
from SymbolTable import SymbolTable
import unittest

class symboltabletests(unittest.TestCase):

    def setUp(self):
        self.st = SymbolTable()

    def testContains(self):
        self.st.addEntry("loop", 100)
        self.assertTrue(self.st.contains("loop"))
        self.assertFalse(self.st.contains("bobby"))
