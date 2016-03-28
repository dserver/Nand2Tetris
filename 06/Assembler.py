
from Code import Code
import string

class Assembler:

    parserObj = None
    symbolTable = None
    fileWriter = None
    code = Code()

    def __init__(self):
        pass


    def setInstructionAndReturnType(self, instruction):
        '''

        :param instruction: string representing cleaned instruction
        :return: string representing type A, C, L, or J
        '''

        self.parserObj.setInstruction(instruction)
        return self.parserObj.instructionType()


    def setParser(self, p):
        self.parserObj = p

    def setSymbolTable(self, s):
        self.symbolTable = s

    def assemble(self, cleanInstructionList):
        ''' Assembles a list of instructions. Calls assembleInstruction on each one.
        :param cleanInstructionList: final instructions with no comments or whitespace
        :return: assembled instructions as a list
        '''
        assembledInstructions = []
        for instruction in cleanInstructionList:
            instructionType = self.setInstructionAndReturnType(instruction)
            if instructionType is "L":
                continue
            assembledInstruction = self.assembleInstruction(instruction)
            assembledInstructions.append(assembledInstruction)

        return assembledInstructions

    def removeWhiteSpaceOnLine(self, line):
        if (line.find(" ") > -1):
            line = string.join(line.split(), '')

        return line

    def removeCommentsOnLine(self, line):

        comment = line.find("//")
        if (comment > -1):
            line = line[0:comment]

        return line

    def assembleTypeA(self, instruction):
        value = instruction[1:] # @value
        if (str.isdigit(value)):
            value_binary = self.code.value(int(value))
            return value_binary
        else:
            if (self.symbolTable.contains(value)):
                addr = self.symbolTable.getAddress(value)
                addr_binary_correct_length = self.code.value(addr)
                binaryInstruction = addr_binary_correct_length
                return binaryInstruction
            else:
                raise RuntimeError("Symbol not found")

    def assembleTypeJ(self, instruction):
        jmp = self.parserObj.jmp()
        comp = self.parserObj.comp()
        dest = "null"

        jmp_binary = self.code.jmp(jmp)
        comp_binary = self.code.comp(comp)
        dest_binary = self.code.dest(dest)

        return str(bin(jmp_binary | comp_binary | dest_binary))

    def assembleTypeC(self, instruction):
        comp = self.parserObj.comp()
        dest = self.parserObj.dest()
        jmp = "null"

        comp_binary = self.code.comp(comp)
        dest_binary = self.code.dest(dest)
        jmp_binary = self.code.jmp(jmp)

        return str(bin(jmp_binary | comp_binary | dest_binary))

    def assembleInstruction(self, instruction):
        '''
        Assembles a single instruction. Symbol table must be initialized with the correct
        symbols and values PRIOR to calling this function by doing a firstPass and then
        a secondPass
        :param instruction: instruction with no whitespace
        :return: binary equivalent
        '''

        instructionType = self.setInstructionAndReturnType(instruction)

        if (instructionType is "L"):
            raise RuntimeError("Cannot assemble type L instruction.")

        if (instructionType == "A"):
            return self.assembleTypeA(instruction)
        elif (instructionType == "J"):
            return self.assembleTypeJ(instruction)
        elif (instructionType == "C"):
            return self.assembleTypeC(instruction)

    def firstPass(self, cleanInstructionList):
        '''
        Sets up symbols for loops by adding each symbol to the table with the proper
        ROM address for the next instruction. For testing, returns the address of the next
        instruction that would be assembled.
        :param cleanInstructionList:
        :return: last ROM address + 1
        '''
        if (self.symbolTable is None):
            raise RuntimeError("Symbol table must be set before first pass.")

        locationCounter = 0

        for instruction in cleanInstructionList:
            instructionType = self.setInstructionAndReturnType(instruction)
            if instructionType is not "L":
                locationCounter += 1
            else:
                self.symbolTable.addEntry(instruction[1:-1], locationCounter)

        return locationCounter

    def secondPass(self, cleanInstructionList):
        '''
        Performs symbol look up on user variables by
        giving each a proper address in the symbol table.
        :param cleanInstructionList: instructions with no whitespace
        :return: address of final variable + 1
        '''
        locationCounter = 16

        for unassembledInstruction in cleanInstructionList:
            instructionType = self.setInstructionAndReturnType(unassembledInstruction)

            if instructionType is "A" and self.parserObj.isSymbolicAInstruction(unassembledInstruction):
                if not self.symbolTable.contains(unassembledInstruction[1:]):
                    self.symbolTable.addEntry(unassembledInstruction[1:], locationCounter)

        return locationCounter






