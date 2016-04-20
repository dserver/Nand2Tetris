import unittest
from VirtualMachine.CodeWriter import CodeWriter
from VirtualMachine.Parser import Parser

class testCodeWriter(unittest.TestCase):


    def setUp(self):
        p = Parser()
        self.codewriter = CodeWriter(p)

    def testArithmeticAdd(self):
        instruction = "add"
        translated = self.codewriter.translateArithmetic(instruction)
        correct_translate = ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=D+M",
                             "@SP", "M=M+1"]

        self.assertEqual(translated, correct_translate)

    def testArithmeticOneEqual(self):
        instruction = "eq"
        translated = self.codewriter.translateArithmetic(instruction)
        correct_translate = ['@SP', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M-1', 'A=M', 'D=D-M', '@EQUAL1', 'D;JEQ', '@NOTEQUAL1', '0;JEQ', '(EQUAL1)',
                              '@SP', 'A=M', 'M=0', '@CONTINUE1', '0;JEQ', '(NOTEQUAL1)', '@SP', 'A=M', 'M=-1', '(CONTINUE1)', '@SP', 'M=M+1']
        self.assertEqual(translated, correct_translate)

    def testArithmeticTwoEqual(self):
        instruction = "eq"
        self.codewriter.translateArithmetic(instruction) # first equal translation
        translated = self.codewriter.translateArithmetic(instruction) # second translation

        # labels should have number appended showing which equal we translated
        correct_translate = ['@SP', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M-1', 'A=M', 'D=D-M', '@EQUAL2', 'D;JEQ', '@NOTEQUAL2', '0;JEQ', '(EQUAL2)',
                              '@SP', 'A=M', 'M=0', '@CONTINUE2', '0;JEQ', '(NOTEQUAL2)', '@SP', 'A=M', 'M=-1', '(CONTINUE2)', '@SP', 'M=M+1']
        self.assertEqual(translated, correct_translate)


    def testPushNoOffset(self):
        instruction = "push local 0"
        translated = self.codewriter.translatePushPop(instruction)

        correct_translation = ["@LCL", "A=M", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

        self.assertEqual(translated, correct_translation)

    def testPush2Offset(self):
        instruction = "push local 2"
        translated = self.codewriter.translatePushPop(instruction)

        correct_translation = ["@2", "D=A", "@LCL", "A=M", "A=A+D", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        self.assertEqual(translated, correct_translation)

