import unittest
from Assembler import Assembler
from fakeparser import fakeparser
from fakesymboltable import fakesymboltable

class AssemblerTests(unittest.TestCase):

    def test_assemble(self):
        instructions = ["@2", "A_const", "L", "C_DP1", "C_APDM", "D0", "0JNE"]

        fakeParser = fakeparser()
        fakeSymbolTable = fakesymboltable()
        a = Assembler()
        a.setParser(fakeParser)
        a.setSymbolTable(fakeSymbolTable)
        binary_instruction = a.assembleInstruction(instructions[0])
        self.assertEqual("0b0000000000000010", binary_instruction)




