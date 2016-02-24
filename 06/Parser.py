# Author: Jonathan Henk
# The specification for this class was given by the authors.

import string, os


# copies the original assembly file into another file where
# all comments and newlines are removed for easy translation in the 
# parser functions
def copy_and_clean(asm_file):
    cp_file = open(os.getenv('TEMP') + '\\temp_assembly_file.txt', 'w+')
    orig_file = open(asm_file, 'r')
    while(1):
        line = orig_file.readline()
        if (line == ''):
            break

        # remove comments and whitespace
        line = clean_line(line)

        # ... after all processing, write line if its still relevant
        # ie. it has some code in it
        if (line != '' and line != '\n'):
            cp_file.write(line)
            cp_file.flush() # garbage gets written sometimes. Not sure why

    orig_file.close()

    return cp_file

def clean_line(line):
    # remove comments
    comment = line.find("//")
    if (comment > -1):
        line = line[0:comment]

    # # remove newline
    # newline = line.find("\n")
    # if (newline > -1):
    #     line = line[0:newline]

    # remove white space
    if (line.find(" ") > -1):
        line = string.join(line.split(), '') + "\n" # hacky way to get newline back in there

    return line

class Parser:
    command = "" # current command


    def __init__(filename):
        this.asm_file = open(filename, 'r')

    # returns if there are any commands left to parse
    def hasMoreCommands():
        spot = this.asm_file.tell() # save place holder at current line
        com = this.asm_file.readline()


        if (com == ''):
            return False
        else:
            this.asm_file.seek(spot) # jump back to place before readline()
            return True

    # read next command. Skips whitespace and comments
    def advance():
        com = this.asm_file.readline()

        if (str.find(com, '=') >= 0): # X=Y type command
            a=1
        else if (str.find(com, ';') >= 0): # D;JMP command
            a=1
        else # ....

    def symbol():

    def dest():

    def comp():

    def jmp():



Parser:
    Constructor(file) - open file and get ready to parse!

    hasMoreCommands - true of stream isn't empty
    advance - read next command from input and sets it to current command

    commandType - returns type of current command
                    A_COMMAND, C_COMMAND, L_COMMAND [ for (xxx) commands]

    symbol - returns symbol or decimal of current command only if
             current command is of type A_COMMAND or L_COMMAND
             returns the @xxx (xxx) xxx part

    dest - returns the dest mnemonic in the current C_COMMAND
           8 possiblities
           
    comp - returns the comp mnemonic in the current C_COMMAND
            some number of possibilities
    jmp - returns the jmp mnemonic in the current C_COMMAND


Code:
    dest - returns binary form of dest
    comp - same
    jump - same