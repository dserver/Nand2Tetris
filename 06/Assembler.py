
from Code import Code

class Assembler:

    parserObj = None
    symbolTable = None
    code = Code()

    def __init__(self):
        pass

    def setParser(self, p):
        self.parserObj = p

    def setSymbolTable(self, s):
        self.symbolTable = s

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


