
from Assembler import Assembler
from Parser import Parser
from SymbolTable import SymbolTable
import sys


# initialize assembler
assembler = Assembler()
parser = Parser()
symbolTable = SymbolTable()

assembler.setParser(parser)
assembler.setSymbolTable(symbolTable)


# open source file
filename = sys.argv[1].split(".")[0]
asmFile = open(sys.argv[1])

# get instructions for assembler from source
# and remove whitespace and comments as well
instructions = []
for line in asmFile:
    line = assembler.removeCommentsOnLine(line)
    line = assembler.removeWhiteSpaceOnLine(line)
    if line != "" and line != "\n":
        instructions.append(line)

asmFile.close()


# Assemble the instructions!
assembler.firstPass(instructions)
assembler.secondPass(instructions)
binaryInstructions = assembler.assemble(instructions)


# write to output
hack_file = open(filename + ".hack", "w+")
for line in binaryInstructions:
    hack_file.write(line[2:] + '\n')
hack_file.close()

