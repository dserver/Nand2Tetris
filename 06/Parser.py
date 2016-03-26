
class Parser:

    commandType = ""
    instruction = ""

    def comp(self):
        if self.commandType == "C":
            (dest, com) = self.instruction.split("=")
            return com
        elif self.commandType == "J":
            (com, jmp) = self.instruction.split(";")
        return com

    def dest(self):
        if self.commandType == "C":
            (dest, com) = self.instruction.split("=")
            return dest

    def instructionType(self):
        return self.commandType

    def jmp(self):
        if self.commandType == "J":
            (com, jmp) = self.instruction.split(";")
            return jmp

    def setInstruction(self, instruction):
        if (instruction.find('=') > -1):
            self.commandType = "C"
        elif (instruction.find(';') > -1):
            self.commandType = "J"
        elif (instruction.find("@") > -1):
            self.commandType = "A"
        elif (instruction.find("(") > -1):
            self.commandType = "L"

        self.instruction = instruction