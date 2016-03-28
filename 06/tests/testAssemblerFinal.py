import unittest
from Assembler import Assembler
from Parser import Parser
from SymbolTable import SymbolTable

class TestAssemblerFinal(unittest.TestCase):

    def setUp(self):
        self.assembler = Assembler()
        parser = Parser()
        self.symbolTable = SymbolTable()

        self.assembler.setSymbolTable(self.symbolTable)
        self.assembler.setParser(parser)

    def testFirstPassSimpleLoop(self):
        instructions = ["(loop)", "@loop", "0;JNE"]
        self.assembler.firstPass(instructions)

        self.assertTrue(self.symbolTable.contains("loop"))
        self.assertEqual(self.symbolTable.getAddress("loop"), 0)

    def testFirstPassComplexLoops(self):
        instructions = ["(loop)", "@loop", "0;JNE", "(bob)", "D=D+1", "(tim)", "M=A+D"]
        self.assembler.firstPass(instructions)

        self.assertTrue(self.symbolTable.contains("loop"))
        self.assertTrue(self.symbolTable.contains("bob"))
        self.assertTrue(self.symbolTable.contains("tim"))
        self.assertEqual(self.symbolTable.getAddress("loop"), 0)
        self.assertEqual(self.symbolTable.getAddress("bob"), 2)
        self.assertEqual(self.symbolTable.getAddress("tim"), 3)

    def testFirstPassMaxAsm(self):
        instructions = ["@R0", "D=M", "@R1", "D=D-M", "@OUTPUT_FIRST", "D;JGT", "@R1", "D=M", "@OUTPUT_D", "0;JMP",
                        "(OUTPUT_FIRST)", "@R0", "D=M", "(OUTPUT_D)", "@R2", "M=D", "(INFINITE_LOOP)",
                        "@INFINITE_LOOP", "0;JMP"]
        self.assembler.firstPass(instructions)
        self.assertTrue(self.assembler.symbolTable.contains("OUTPUT_FIRST"))

        self.assertEqual(self.assembler.symbolTable.getAddress("OUTPUT_FIRST"), 10)

    def testFirstPassMaxAsmInfiniteLoopAddress(self):
        instructions = ["@R0", "D=M", "@R1", "D=D-M", "@OUTPUT_FIRST", "D;JGT", "@R1", "D=M", "@OUTPUT_D", "0;JMP",
                        "(OUTPUT_FIRST)", "@R0", "D=M", "(OUTPUT_D)", "@R2", "M=D", "(INFINITE_LOOP)",
                        "@INFINITE_LOOP", "0;JMP"]
        self.assembler.firstPass(instructions)
        self.assertTrue(self.assembler.symbolTable.contains("INFINITE_LOOP"))

        self.assertEqual(self.assembler.symbolTable.getAddress("INFINITE_LOOP"), 14)

    def testSecondPassMaxAsmInfiniteLoopAddress(self):
        instructions = ["@R0", "D=M", "@R1", "D=D-M", "@OUTPUT_FIRST", "D;JGT", "@R1", "D=M", "@OUTPUT_D", "0;JMP",
                        "(OUTPUT_FIRST)", "@R0", "D=M", "(OUTPUT_D)", "@R2", "M=D", "(INFINITE_LOOP)",
                        "@INFINITE_LOOP", "0;JMP"]
        self.assembler.firstPass(instructions)
        self.assembler.secondPass(instructions)
        self.assertTrue(self.assembler.symbolTable.contains("INFINITE_LOOP"))

        self.assertEqual(self.assembler.symbolTable.getAddress("INFINITE_LOOP"), 14)

    def testSecondPassSimple(self):
        instructions = ["(loop)", "@myVar", "M=5", "@loop", "0;JNE"]
        self.assembler.firstPass(instructions)
        self.assembler.secondPass(instructions)

        self.assertTrue(self.symbolTable.contains("loop"))
        self.assertTrue(self.symbolTable.contains("myVar"))
        self.assertEqual(self.symbolTable.getAddress("myVar"), 16)
        self.assertEqual(self.symbolTable.getAddress("loop"), 0)


    def testAssembleInstructions(self):
        instructions = ["(loop)", "@loop", "0;JEQ"]
        self.assembler.firstPass(instructions)
        self.assembler.secondPass(instructions)
        self.assertEqual(["0b0000000000000000", "0b1110101010000010"],
                         self.assembler.assemble(instructions))


    # def testAssembleInstructionsWithComments(self):
    #     instructions = ["(loop)", "// some comment", "@loop", "// another comment", "0;JEQ"]
    #     self.assembler.firstPass(instructions)
    #     self.assembler.secondPass(instructions)
    #     self.assertEqual(["0b0000000000000000", "0b1110101010000010"],
    #                      self.assembler.assemble(instructions))
    #


