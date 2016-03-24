from AbstractFileReaderWriter import AbstractFileReaderWriter

class FakeFileReaderWriter(AbstractFileReaderWriter):

    linesInFakeFile = []
    currentLine = 0

    def __init__(self, lineList):
        self.linesInFakeFile = lineList

    def hasNext(self):
        if (self.currentLine == len(self.linesInFakeFile)):
            return False
        return True


    def advance(self):
        self.currentLine += 1


    def writeLine(self, string):
        self.linesInFakeFile.append(string)


    def readLine(self):
        if (self.hasNext()):
            return self.linesInFakeFile[self.currentLine]


    def open(self, filename):
        pass


    def close(self, filename):
        pass