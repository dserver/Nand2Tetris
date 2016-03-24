
class AbstractFileReaderWriter:
    """ provides a common interface to object which are files """

    currentFile = None


    def hasNext(self):
        raise NotImplementedError("Should implement this.")


    def advance(self):
        raise NotImplementedError("Should implement this.")


    def writeLine(self, string):
        raise NotImplementedError("Should implement this.")


    def readLine(self):
        raise NotImplementedError("Should implement this.")


    def open(self, filename):
        raise NotImplementedError("Should implement this.")


    def close(self, filename):
        raise NotImplementedError("Should implement this.")