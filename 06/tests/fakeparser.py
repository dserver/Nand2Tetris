
class fakeparser:


    """ Pass instructionType "A_symbol" for @value
                             "A_const" for @1300
                             "L" for (loop)
                             "C_DP1" for D=D+1
                              "C_APDM" for A=D+M
                              "D0" for D=0
                              "0JNE" for 0;JNE

    """
    fakeDest = ""
    fakeJmp = ""
    fakeComp = ""
    fakeInstructionType = ""
    def __init__(self):
        pass

    def setInstruction(self, instruction):
        if (instruction.find("@") > -1):
            self.fakeInstructionType = "A"
        elif (instruction == "A_const"):
            self.fakeInstructionType = "A"
        elif (instruction == "L"):
            self.fakeInstructionType = "L"
        elif (instruction == "D=D+1"):
            self.fakeDest = "D"
            self.fakeComp = "D+1"
            self.fakeInstructionType = "C"
        elif (instruction == "A=D+M"):
            self.fakeDest = "A"
            self.fakeComp = "D+M"
            self.fakeInstructionType = "C"
        elif (instruction == "D0"):
            self.fakeDest = "D"
            self.fakeComp = "0"
            self.fakeInstructionType = "C"
        elif (instruction == "D0"):
            self.fakeDest = "D"
            self.fakeComp = "0"
            self.fakeInstructionType = "C"
        elif (instruction == "0;JNE"):
            self.fakeComp = "0"
            self.fakeJmp = "JNE"
            self.fakeInstructionType = "J"

    def dest(self):
        return self.fakeDest

    def jmp(self):
        return self.fakeJmp

    def comp(self):
        return self.fakeComp

    def instructionType(self):
        return self.fakeInstructionType