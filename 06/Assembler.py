
from Code import Code
import string

class Assembler:

    parserObj = None
    symbolTable = None
    fileWriter = None
    code = Code()

    def __init__(self):
        pass

    def setParser(self, p):
        self.parserObj = p

    def setSymbolTable(self, s):
        self.symbolTable = s

    def assemble(self, instructionList):
        assembledInstructions = []
        for instruction in instructionList:
            assembledInstructions.append(self.assembleInstruction(instruction))

        return assembledInstructions

    def removeWhiteSpaceOnLine(self, line):
                # remove white space
        if (line.find(" ") > -1):
            line = string.join(line.split(), '')

        return line

    def removeCommentsOnLine(self, line):
        # remove comments
        comment = line.find("//")
        if (comment > -1):
            line = line[0:comment]

        return line

    def assembleInstruction(self, instruction):
        self.parserObj.setInstruction(instruction)
        command_type = self.parserObj.instructionType()

        binaryInstruction = ""

        if (command_type == "A"):
            value = instruction[1:]
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
        elif (command_type == "L"):
            return ""
        elif (command_type == "J"):
            jmp = self.parserObj.jmp()
            comp = self.parserObj.comp()
            dest = "null"
            jmp_binary = self.code.jmp(jmp)
            comp_binary = self.code.comp(comp)
            dest_binary = self.code.dest(dest)
            return str(bin(jmp_binary | comp_binary | dest_binary))
        elif (command_type == "C"):
            comp = self.parserObj.comp()
            dest = self.parserObj.dest()
            jmp = "null"
            comp_binary = self.code.comp(comp)
            dest_binary = self.code.dest(dest)
            jmp_binary = self.code.jmp(jmp)
            return str(bin(jmp_binary | comp_binary | dest_binary))



