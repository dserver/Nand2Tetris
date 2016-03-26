import unittest
from Assembler import Assembler
from fakeparser import fakeparser
from fakesymboltable import fakesymboltable

class AssemblerTests(unittest.TestCase):
    # instructions = ["@2", "A_const", "L", "C_DP1", "C_APDM", "D0", "0JNE"]
    def setUp(self):
        self.fakeParser = fakeparser()
        self.fakeSymbolTable = fakesymboltable()
        self.assembler = Assembler()
        self.assembler.setParser(self.fakeParser)
        self.assembler.setSymbolTable(self.fakeSymbolTable)

    def test_assemble_A_const(self):

        binary_instruction = self.assembler.assembleInstruction("@2")
        self.assertEqual("0b0000000000000010", binary_instruction)

    def test_assemble_A_sym(self):
        self.fakeSymbolTable.addEntry("loop", 110)
        binary_instruction = self.assembler.assembleInstruction("@loop")
        self.assertEqual("0b0000000001101110", binary_instruction)








