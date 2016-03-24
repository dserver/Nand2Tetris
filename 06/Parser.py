# Author: Jonathan Henk
# The specification for this class was given by the authors.


import unittest
from AbstractInstructionFile import AbstractInstructionFile


class Parser:
    """ Parses instructions from an instructions file. Used to
    get instruction type, next instruction, and fields within the 
    instruction type"""


    currentCommandBeingParsed = "" # current command
    commandType = ""
    instructionsFile = None


    def __init__(self, instructionFile):
        self.instructionsFile = instructionFile
        if (instructionFile.hasNext()):
            self.currentCommandBeingParsed = instructionFile.getInstruction()
            self.setCurrentCommandType(self.currentCommandBeingParsed)
        


    # returns if there are any commands left to parse
    def hasMoreCommands(self):
        return self.instructionsFile.hasNext()


    # read next command. Skips whitespace and comments
    def readNextLine(self):
        if (self.hasMoreCommands()):
            self.instructionsFile.advance()
            self.currentCommandBeingParsed = self.instructionsFile.getInstruction()
            self.setCurrentCommandType(self.currentCommandBeingParsed)



    def setCurrentCommandType(self, command):
        if (command.find('=') > -1 or command.find(';') > -1):
            self.commandType = "C_COMMAND"
        elif (command.find("@") > -1):
            self.commandType = "A_COMMAND"
        elif (command.find("(") > -1):
            self.commandType = "L_COMMAND"



    def symbolIn_L_or_A_command(self):
        if (self.commandType == "L_COMMAND"):
            return self.currentCommandBeingParsed[1:-1]
        elif (self.commandType == "A_COMMAND"):
            return self.currentCommandBeingParsed[1:]


    def destIn_C_command(self):
        if (self.commandType == "C_COMMAND"):
            if (self.currentCommandBeingParsed.find("=") > -1):
                (dest, com) = self.currentCommandBeingParsed.split("=")
                return dest


    def compIn_C_command(self):
        if (self.commandType == "C_COMMAND"):
            if (self.currentCommandBeingParsed.find("=") > -1):
                (dest, com) = self.currentCommandBeingParsed.split("=")
                return com
            elif (self.currentCommandBeingParsed.find(";") > -1):
                (dest, jmp) = self.currentCommandBeingParsed.split(";")
                return dest

    def jmpIn_C_command(self):
        if (self.commandType == "C_COMMAND"):
            if (self.currentCommandBeingParsed.find(";") > -1):
                (dest, jmp) = self.currentCommandBeingParsed.split(";")
                return jmp


    def getCommandType(self):
        return self.commandType


    def getCurrentCommand(self):
        return self.currentCommandBeingParsed



class ParserTests(unittest.TestCase):
    """ Unit tests for Parser class"""

    def testHasMoreCommands(self):
        instructionFile = TestAssemblyFile(["@100 D=1 M=A+1"])
        p = Parser(instructionFile)
        self.assertEquals(p.hasMoreCommands(), True, 'should have more commands')



    def testNoMoreCommands(self):
        instructionFile = TestAssemblyFile([])
        p = Parser(instructionFile)
        self.assertEquals(p.hasMoreCommands(), False, 'shouldn\'t have more commands')



    def testGetCurrentCommand(self):
        instructionFile = TestAssemblyFile(["@100 D=1"])
        p = Parser(instructionFile)
        self.assertEquals(p.getCurrentCommand(), "@100", 'current command incorrect')


    def testReadNextLine(self):
        instructionFile = TestAssemblyFile(["@100 D=1 M=A+1"])
        p = Parser(instructionFile)
        p.readNextLine()
        self.assertEquals(p.getCurrentCommand(), "D=1", 'current command should be D=1')



    def testCommandTypeC(self):
        instructionFile = TestAssemblyFile(["A=D+1"])
        p = Parser(instructionFile)
        self.assertEquals(p.getCommandType(), "C_COMMAND", 'should be C command')



    def testCommandTypeA(self):
        instructionFile = TestAssemblyFile(["@xyz"])
        p = Parser(instructionFile)
        self.assertEquals(p.getCommandType(), "A_COMMAND", 'should be A command')



    def testCommandTypeL(self):
        instructionFile = TestAssemblyFile(["(loop1)"])
        p = Parser(instructionFile)
        self.assertEquals(p.getCommandType(), "L_COMMAND", 'should be L command')



    def testCorrectSymbolInDestCompCommand(self):
        instructionFile = TestAssemblyFile(["A=D+1"])
        p = Parser(instructionFile)
        self.assertEquals(p.compIn_C_command(), "D+1", 'comp should be d+1')
        self.assertEquals(p.destIn_C_command(), "A", 'comp should be A')



    def testCorrectSymbolInJumpCompCommand(self):
        instructionFile = TestAssemblyFile(["D;JNE"])
        p = Parser(instructionFile)
        self.assertEquals(p.compIn_C_command(), "D", 'comp should be d')
        self.assertEquals(p.jmpIn_C_command(), "JNE", 'comp should be JNE')


if __name__ == '__main__':
    from TestAssemblyFile import TestAssemblyFile
    unittest.main()