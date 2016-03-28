import unittest
from Assembler import Assembler
from fakeparser import fakeparser
from fakesymboltable import fakesymboltable

class TestAssembler(unittest.TestCase):
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


    def test_jumpInstruction(self):
        binary_instruction = self.assembler.assembleInstruction("0;JNE")
        self.assertEqual("0b1110101010000101", binary_instruction)

    def test_D_eq_DplusOne(self):
        binary_instruction = self.assembler.assembleInstruction("D=D+1")
        self.assertEqual("0b1110011111010000", binary_instruction)


    def test_A_eq_DPlusM(self):
        binary_instruction = self.assembler.assembleInstruction("A=D+M")
        self.assertEqual("0b1111000010100000", binary_instruction)

    def testRemoveWhiteSpaceOnLine(self):
        r = self.assembler.removeWhiteSpaceOnLine("   A   =   D  + 1 //a comment")
        self.assertEqual("A=D+1//acomment", r)


    def testRemoveCommentsOnLine(self):
        r = self.assembler.removeCommentsOnLine("   A   =   D  + 1 //a comment")
        self.assertEqual("   A   =   D  + 1 ", r)


    def testAssemble(self):
        instructions = ["@2", "0;JNE", "D=D+1", "A=D+M"]
        assembledInstructions = self.assembler.assemble(instructions)
        self.assertEqual(["0b0000000000000010", "0b1110101010000101", "0b1110011111010000", "0b1111000010100000"],
                         assembledInstructions)

    def testAssembleWithSymbolicA(self):
        # symbol table already initialized in setUp() to return 110 for any symbol
        instructions = ["@2", "0;JNE", "@myVariable", "D=D+1", "A=D+M"]
        assembledInstructions = self.assembler.assemble(instructions)
        self.assertEqual(["0b0000000000000010", "0b1110101010000101", "0b0000000001101110",
                          "0b1110011111010000", "0b1111000010100000"],
                         assembledInstructions)

    def testFirstPass(self):
        instructions = ["@2", "0;JNE", "@userSymbol", "D=D+1", "A=D+M"]
        self.assertEqual(5, self.assembler.firstPass(instructions))

    # def testSecondPass(self):
    #     instructions = ["(loop)", "@loop", "0;JEQ"]
    #     self.assertEqual(["0b0000000000000000", "0b1110101010000010"], self.assembler.secondPass(instructions))
    #


