import unittest
from Parser import Parser

class parsertests(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_InstructionTypeA(self):
        self.parser.setInstruction("@symbol")
        self.assertEqual("A", self.parser.instructionType())

    def test_InstructionTypeC(self):
        self.parser.setInstruction("D=D+1")
        self.assertEqual("C", self.parser.instructionType())

    def test_InstructionTypeL(self):
        self.parser.setInstruction("(loop)")
        self.assertEqual("L", self.parser.instructionType())

    def test_InstructionTypeL(self):
        self.parser.setInstruction("0;JNE")
        self.assertEqual("J", self.parser.instructionType())

    def testComp(self):
        self.parser.setInstruction("0;JNE")
        self.assertEqual("0", self.parser.comp())

        self.parser.setInstruction("D=D+1")
        self.assertEqual("D+1", self.parser.comp())

    def testDest(self):
        self.parser.setInstruction("D=D+1")
        self.assertEqual("D", self.parser.dest())


    def testJump(self):
        self.parser.setInstruction("0;JNE")
        self.assertEqual("JNE", self.parser.jmp())

    def testIsSymbolicAInstruction(self):
        self.assertTrue(self.parser.isSymbolicAInstruction("@symbol"))
        self.assertFalse(self.parser.isSymbolicAInstruction("@100"))