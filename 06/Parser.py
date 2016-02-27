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

        # after all processing, write line to final assembly file if its still relevant
        # ie. the line will translate to a binary instruction
        if (line != '' and line != '\n'):
            cp_file.write(line)
            cp_file.flush() # garbage gets written sometimes. Not sure why

    orig_file.close()
    cp_file.close()
    return

# removes all comments and whitespace
def clean_line(line):
    # remove comments
    comment = line.find("//")
    if (comment > -1):
        line = line[0:comment]

    # remove white space
    if (line.find(" ") > -1):
        line = string.join(line.split(), '') + "\n" # hacky way to get newline back in there

    return line

class Parser:

    commands = [] # each line in the input assembly file is stored here
    command = "" # current command
    command_i = 0 # which 'line' in the file we're on
    commandType = ""


    def __init__(self, filename):
        copy_and_clean(filename)
        asm_file = open(os.getenv('TEMP') + '\\temp_assembly_file.txt', 'r')
        for line in asm_file:
            if (line.find('\n') > -1):
                self.commands.append(line[:-1])
            else:
                self.commands.append(line)

        # hacky way to get first command read
        self.command_i = -1 
        self.advance()


    # returns if there are any commands left to parse
    def hasMoreCommands(self):
        if (self.command_i == len(self.commands)):
            return False
        return True


    # read next command. Skips whitespace and comments
    def advance(self):
        self.command_i += 1
        self.command = commands[self.command_i]
        if (self.command.find('=') > -1 or self.command.find(';') > -1):
            self.commandType = "C_COMMAND"
        elif (self.command.find("@") > -1):
            self.commandType = "A_COMMAND"
        elif (self.command.find("(") > -1):
            self.commandType = "L_COMMAND"


    def symbol(self):
        if (self.commandType == "L_COMMAND"):
            return self.command[1:-1]
        elif (self.commandType == "A_COMMAND"):
            return self.command[1:]


    def dest(self):
        if (self.commandType == "C_COMMAND"):
            if (self.command.find("=") > -1):
                (com, dest) = self.command.split("=")
                return dest
            elif (self.command.find(";") > -1):
                (dest, jmp) = self.command.split(";")
                return dest


    def comp(self):
        if (self.commandType == "C_COMMAND"):
            if (self.command.find("=") > -1):
                (com, dest) = self.command.split("=")
                return com


    def jmp(self):
        if (self.commandType == "C_COMMAND"):
            if (self.command.find(";") > -1):
                (dest, jmp) = self.command.split(";")
                return jmp