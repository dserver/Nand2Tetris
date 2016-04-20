from CodeWriter import CodeWriter
from Parser import Parser

import sys
import os.path
import os


def hasNewLine(line):
    if str.find(line, '\n') < 0:
        return False
    else:
        return True



def translateFile(vm_file):
    parser = Parser()
    codeWriter = CodeWriter(parser)
    codeWriter.setFileName(vm_file)

    hack_file_name = vm_file[:-3] + ".hack"
    hack_file = open(hack_file_name, "w+")

    with open(vm_file) as f:
        for nextLine in f:
            if hasNewLine(nextLine):
                nextLine = nextLine[:-1]

            print nextLine
            asm_instructions = codeWriter.translate(nextLine)

            hack_file.writelines(asm_instructions)

        hack_file.close()




if os.path.isfile(sys.argv[1]):
    translateFile(sys.argv[1])



