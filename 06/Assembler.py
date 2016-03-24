from Parser import Parser
from Code import Code
import sys
import unittest

class Assembler:

    sourceFile = None
    destinationFile = None

    currentInstruction = ""
    currentInstructionAssembled = ""

    def __init__(self, sourceFile, destinationFile):
        self.sourceFile = sourceFile
        self.destinationFile = destinationFile


    """
    Returns '0bxxxxxxxxxxxx', the binary string of instruction """
    def assembleInstruction(self, instruction):
        pass

    """
    Write binary instruction to destination file """
    def writeInstruction(self, instruction):
        pass

    """ Assemble sourceFile and output to sourceFile.hack """
    def assemble(self):
        pass

    def assembleNextInstruction(self):
        pass

    def hasNextInstruction(self):
        pass




class AssemblerTest(unittest.TestCase):

    def testAssembleInstruction(self):
        testSourceFile = FakeFileReaderWriter(["A=1", "D=0", "@100"])
        testDestinationFile = FakeFileReaderWriter([])
        a = Assembler(testSourceFile, testDestinationFile)
        self.assertEquals(a.assembleNextInstruction(),
                          '0b1110111111100000', "Output instruction incorrect")

        self.assertEquals(a.assembleNextInstruction(),
                          '0b1110101010010000', "Output instruction incorrect")



    def testHasNextInstruction(self):
        testSourceFile = FakeFileReaderWriter(["A=1", "D=0", "@100"])
        testDestinationFile = FakeFileReaderWriter([])
        a = Assembler(testSourceFile, testDestinationFile)
        self.assertEquals(a.hasNextInstruction(),
                          True, "Should have next instruction")



    def testNoNextInstruction(self):
        testSourceFile = FakeFileReaderWriter([])
        testDestinationFile = FakeFileReaderWriter([])
        a = Assembler(testSourceFile, testDestinationFile)
        self.assertEquals(a.hasNextInstruction(), False, "Should be no next instruction")



    def testNoNextInstructionAfterAdvancingToEnd(self):
        testSourceFile = FakeFileReaderWriter(["A=1"])
        testDestinationFile = FakeFileReaderWriter([])
        a = Assembler(testSourceFile, testDestinationFile)
        a.assembleNextInstruction()
        self.assertEquals(a.hasNextInstruction(), False, "Should be no next instruction")



    def testWriteAssembledInstruction(self):
        testSourceFile = FakeFileReaderWriter(["A=1", "D=0", "@100"])
        testDestinationFile = FakeFileReaderWriter([])
        a = Assembler(testSourceFile, testDestinationFile)
        a.writeInstruction('0b1110111111100000')
        self.assertEquals(testDestinationFile.readLine(), '0b1110111111100000', 
            "Failed to write correct instruction")


if __name__ == "__main__":
    from FakeFileReaderWriter import FakeFileReaderWriter

    unittest.main()
