
from VirtualMachine.Parser import Parser
import unittest

class testParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def testCommandType(self):
        self.assertEqual(self.parser.commandType("add"), self.parser.C_ARITHMETIC)
        self.assertEqual(self.parser.commandType("push local 0"), self.parser.C_PUSH)
        self.assertEqual(self.parser.commandType("pop temp 1"), self.parser.C_POP)

    def testArgsWithPush(self):
        instruction = "pop local 2"
        self.parser.setInstruction(instruction)
        self.assertEqual(self.parser.arg1(), "local")
        self.assertEqual(self.parser.arg2(), "2")


    def testArg0Push(self):
        instruction = "push local 0"
        self.parser.setInstruction(instruction)
        self.assertEqual(self.parser.arg0(), "push")



