
class AbstractInstructionFile:
    """ Provides interface for parser object to retrieve instructions
    from """

    def hasNextInstruction(self):
        raise NotImplementedError("Should implement this.")

    def advance(self):
        raise NotImplementedError("Should implement this.")

    def getInstruction(self):
        raise NotImplementedError("Should implement this.")