from Parser import Parser

class CodeWriter:


    def __init__(self, parser):
        '''
        Opens the output file and gets ready to write into it
        :param parser object to use
        :return:
        '''
        self.parser = Parser()
        self.eqCounter = 0 # appended to end of EQUAL labels so they are unique
        self.memoryMappedRegisters = {"local": "LCL",
                       "argument": "ARG",
                       "this": "R3",
                       "that": "R4",
                       "pointer": "R3",
                        "temp": "R5"}

        self.currentVMFile = ""
        self.file = None





    def setCurrentVMFile(self, fileName):
        '''
        Changes VM file that is currently being translated
        :param fileName:
        :return:
        '''
        self.currentVMFile = fileName[:-3]




    def assembleVMCommand(self, command):
        self.parser.setInstruction(command)
        if self.parser.commandType(command) == 0:
            return self.translateArithmetic(command)
        elif self.parser.commandType(command) in range(1,3):
            return self.translatePushPop(command)




    def translateArithmetic(self, command):
        '''
        Writes the assembly code that is the translation of the given
        arithmetic command
        :param command: command string
        :return: list where each element is one line of assembly code

        :todo "sub", "neq", "gt", "lt", "and", "or", "not"]
        '''
        self.parser.setInstruction(command)
        if self.parser.currentInstructionType != self.parser.C_ARITHMETIC:
            raise RuntimeError("translate arithmetic cannot translate non-arithmetic type")

        if command == "add":
            return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=D+M",
                             "@SP", "M=M+1"]
        elif command == "sub":
            return ["@SP", "A=M", "A=A-1", "D=M", "A=A-1", "M=M-D", "@SP", "M=M-1"]
        elif command == "neg":
            return ["@SP", "A=M", "A=A-1", "M=-M"]
        elif command == "and":
            return ["@SP", "A=M", "A=A-1", "D=M", "A=A-1", "M=D&M", "@SP", "M=M-1"]
        elif command == "or":
            return ["@SP", "A=M", "A=A-1", "D=M", "A=A-1", "M=D|M", "@SP", "M=M-1"]
        elif command == "not":
            return ["@SP", "A=M", "M=!M"]
        elif command == "gt":
            self.eqCounter += 1
            return ["@SP", "A=M", "A=A-1", "D=M", "A=A-1", "D=M-D", "@GT" + str(self.eqCounter), "D;JGT", "@NGT" + str(self.eqCounter),
                    "0;JEQ", "(GT"   + str(self.eqCounter) + ")", "@SP", "A=M", "A=A-1", "A=A-1", "M=-1", "@SP", "M=M-1",
                    "@CONTINUE" + str(self.eqCounter), "0;JEQ", "(NGT"  + str(self.eqCounter) + ")", "@SP", "A=M", "A=A-1",
                    "A=A-1", "M=0", "@SP", "M=M-1", "@CONTINUE" + str(self.eqCounter), "0;JEQ", "(CONTINUE"  + str(self.eqCounter) + ")"]
        elif command == "lt":
            self.eqCounter += 1
            return ["@SP", "A=M", "A=A-1", "D=M", "A=A-1", "D=M-D", "@LT" + str(self.eqCounter), "D;JLT",
                    "@NLT" + str(self.eqCounter), "0;JEQ", "(LT"   + str(self.eqCounter) + ")", "@SP", "A=M", "A=A-1",
                    "A=A-1", "M=-1", "@SP", "M=M-1", "@CONTINUE" + str(self.eqCounter), "0;JEQ",
                    "(NLT"  + str(self.eqCounter) + ")", "@SP", "A=M", "A=A-1", "A=A-1", "M=0", "@SP", "M=M-1",
                    "@CONTINUE" + str(self.eqCounter), "0;JEQ", "(CONTINUE"  + str(self.eqCounter) + ")"]
        elif command == "eq":
            self.eqCounter += 1
            return ['@SP', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M-1', 'A=M', 'D=D-M', '@EQUAL' + str(self.eqCounter), 'D;JEQ', '@NOTEQUAL' + str(self.eqCounter), '0;JEQ',
                     '(EQUAL' + str(self.eqCounter) + ')', '@SP', 'A=M', 'M=-1', '@CONTINUE'  + str(self.eqCounter),
                                '0;JEQ', '(NOTEQUAL' + str(self.eqCounter) + ')', '@SP', 'A=M', 'M=0',
                     '(CONTINUE' + str(self.eqCounter) + ')', '@SP', 'M=M+1']




    def translatePushPop(self, command):
        '''
        Return assembly code for a given push/pop VM command, ie push local 2
        Calls translatePush or translatePop depending on type
        :param command:
        :return:
        '''

        self.parser.setInstruction(command)
        if (self.parser.currentInstructionType != self.parser.C_PUSH
            and self.parser.currentInstructionType != self.parser.C_POP):
            raise RuntimeError("Translate Push Pop failed - not C_PUSH or C_POP")

        if self.parser.currentInstructionType == self.parser.C_POP:
            return self.translatePop(command)
        else:
            return self.translatePush(command)





    def translatePush(self, command):
        '''
        return assembly instructions for any push VM command
        :param command:
        :return:
        '''
        self.parser.setInstruction(command)
        VMStackLabel = self.parser.arg1()
        offset = int(self.parser.arg2())
        translatedLabel = "" #  @translatedLabel

        if (VMStackLabel in self.memoryMappedRegisters):
            translatedLabel = self.memoryMappedRegisters[VMStackLabel]
        elif (VMStackLabel == "constant"):
            return self.translatePushConstant(offset)
        else:
            translatedLabel = self.currentVMFile + "." + str(offset)

        if offset == 0:
            return ["@" + VMStackLabel, "A=M", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]


        return ["@" + str(offset), "D=A", "@" + VMStackLabel, "A=M", "A=A+D", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]






    def translatePushConstant(self, constant):
        '''
        Return assembly code for a push constant VM instruction
        :param constant: integer constant
        :return:
        '''

        return ["@" + str(constant), "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]


    def translatePop(self, command):
        self.parser.setInstruction(command)

        label = self.parser.arg1()
        offset = int(self.parser.arg2())

        if (label in self.memoryMappedRegisters):
            label = self.memoryMappedRegisters[label]
        else:
            label = self.currentVMFile + "." + str(offset)

        if offset == 0:
            return ["@SP", "A=M", "A=A-1", "D=M", "@" + label, "A=M", "M=D"]


        instructions = ["@SP", "A=M", "A=A-1", "D=M", "@" + label, "A=M", "M=D"]
        for i in range(0, offset):
            instructions.append("A=A+1")
        instructions.append("M=D")

        return instructions






    def writePushPop(self, command):
        '''
        Writes the assembly code that is a translation of the command
        Only called when command is either C_PUSH or C_POP
        :param command:
        :return:
        '''

        #for line in self.translatePushPop(command):
         #   self.file.write(line + '\n')
        pass




    def close(self):
        '''
        Close output file
        :return:
        '''
        pass
        #self.file.close()