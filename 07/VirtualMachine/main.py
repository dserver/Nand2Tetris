from CodeWriter import CodeWriter
from Parser import Parser

import sys
import os.path
import os
import string

def removeWhiteSpaceOnLine(line):
    if (line.find(" ") > -1):
        line = string.join(line.split(), '')

    return line

def removeCommentsOnLine(line):

    comment = line.find("//")
    if (comment > -1):
        line = line[0:comment]

    return line

def hasNewLine(line):
    if str.find(line, '\n') < 0:
        return False
    else:
        return True



def translateFile(vm_file):
    parser = Parser()
    codeWriter = CodeWriter(parser)
    codeWriter.setCurrentVMFile(vm_file)

    hack_file_name = vm_file[:-3] + ".asm"
    hack_file = open(hack_file_name, "w+")

    with open(vm_file) as f:
        for nextLine in f:
            if hasNewLine(nextLine):
                nextLine = nextLine[:-1]

            nextLine = removeCommentsOnLine(nextLine)
            if (nextLine == ''):
                continue

            print nextLine


            asm_instructions = codeWriter.assembleVMCommand(nextLine)

            for i in xrange(0, len(asm_instructions)):
                asm_instructions[i] = asm_instructions[i] + '\n'

            hack_file.writelines(asm_instructions)

        hack_file.close()




if os.path.isfile(sys.argv[1]):
    translateFile(sys.argv[1])



