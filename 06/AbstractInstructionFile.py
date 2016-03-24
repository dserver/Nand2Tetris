
class AbstractInstructionFile:
    """ Provides interface for modules to read instructions from, but 
    not write """

    def hasNextInstruction(self):
        raise NotImplementedError("Should implement this.")

    def advance(self):
        raise NotImplementedError("Should implement this.")

    def getInstruction(self):
        raise NotImplementedError("Should implement this.")