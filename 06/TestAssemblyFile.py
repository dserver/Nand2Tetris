
from AbstractInstructionFile import AbstractInstructionFile

class TestAssemblyFile(AbstractInstructionFile):

    instructions = []
    currentInstructionIndex = 0

    def __init__(self, instructionList):
        if (len(instructionList) > 0):
            self.instructions = instructionList[0].split()

    def hasNext(self):
        if (self.currentInstructionIndex == len(self.instructions)):
            return False
        return True

    def advance(self):
        self.currentInstructionIndex += 1

    def getInstruction(self):
        return self.instructions[self.currentInstructionIndex]