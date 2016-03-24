
def TestAssemblyFile(AbstractInstructionFile):

    instructions = []
    currentInstructionIndex = 0

    def __init__(self, instructionList):
        self.instructions = instructionList

    def hasNext(self):
        if (currentInstructionIndex == len(self.instructions):
            return False
        return True

    def advance(self):
        self.currentInstructionIndex += 1

    def getInstruction(self):
        return self.instructions[currentInstructionIndex]