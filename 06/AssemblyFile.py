import string, os

class AssemblyFile(AbstractInstructionFile):
    
    def __init__(self, assemblyFile):
        copy_and_clean(filename)
        cleanedFile = open(os.getenv('TEMP') + '\\temp_assembly_file.txt', 'r')

    # copies the original assembly file into another file where
    # all comments and newlines are removed for easy translation in the
    # parser functions
    def copy_and_clean(self, asm_file):
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
    def clean_line(self, line):
        # remove comments
        comment = line.find("//")
        if (comment > -1):
            line = line[0:comment]

        # remove white space
        if (line.find(" ") > -1):
            line = string.join(line.split(), '') + "\n" # hacky way to get newline back in there

        return line


    def hasNext(self):
        pass

    def advance(self):
        pass

    def getInstruction(self):
        pass


