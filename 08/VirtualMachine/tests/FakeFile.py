
class FakeFile:

    def __init__(self, lines=[]):
        self.linesInFile = lines
        self.currentLine = 0


    def read(self):
        return self.linesInFile[self.currentLine]

    def readLine(self):
        return self.linesInFile[self.currentLine]

    def advance(self):
        self.currentLine += 1

    def write(self, string):
        self.linesInFile.append(string)