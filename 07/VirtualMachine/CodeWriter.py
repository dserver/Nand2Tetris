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
        label = self.parser.arg1()
        offset = int(self.parser.arg2())

        if label == "local":
            return self.translatePushLocal(offset)
        elif label == "argument":
            return self.translatePushArgument(offset)
        elif label == "pointer":
            return self.translatePushPointer(offset)
        elif label == "static":
            return self.translatePushStatic(offset)
        elif label == "temp":
            return self.translatePushTemp(offset)
        elif label == "this":
            return self.translatePushThis(offset)
        elif label == "that":
            return self.translatePushThat(offset)
        elif label == "constant":
            return self.translatePushConstant(offset)


    def translatePopTemp(self, constant):
        '''

        :param constant: integer
        :return:
        '''

        return ["@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@" + str(5 + constant),
                "M=D"]






    def translatePopThat(self, constant):
        '''

        :param constant: integer
        :return:
        '''

        asm_incomplete = ["@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@THAT",
                "A=M"]

        for i in xrange(0,constant):
            asm_incomplete.append("A=A+1")

        asm_incomplete.append("M=D")
        return asm_incomplete






    def translatePopThis(self, constant):
        '''

        :param constant: integer
        :return:
        '''

        asm_incomplete = ["@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@THIS",
                "A=M"]

        for i in xrange(0,constant):
            asm_incomplete.append("A=A+1")

        asm_incomplete.append("M=D")
        return asm_incomplete


    def translatePopArgument(self, constant):
        '''

        :param constant: integer
        :return:
        '''

        asm_incomplete = ["@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@ARG",
                "A=M"]

        for i in xrange(0,constant):
            asm_incomplete.append("A=A+1")

        asm_incomplete.append("M=D")
        return asm_incomplete


    def translatePopPointer(self, constant):
        '''

        :param constant: integer
        :return:
        '''
        return ["@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@" + str(3 + constant),
                "M=D"]


    def translatePopLocal(self, constant):
        '''

        :param constant: integer
        :return:
        '''

        asm = ["@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@LCL",
                "A=M"]

        for i in xrange(0,constant):
            asm.append("A=A+1")

        asm.append("M=D")
        return asm


    def translatePopStatic(self, constant):
        '''

        :param constant: integer
        :return:
        '''

        asm = ["@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@" + self.currentVMFile + "." + str(constant),
                "A=M"]

        for i in xrange(0,constant):
            asm.append("A=A+1")

        asm.append("M=D")
        return asm

    def translatePushThat(self, constant):
        '''

        :param constant: integer
        :return:
        '''
        return ["@" + str(constant),
                "D=A",
                "@THAT",
                "A=M",
                "A=A+D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"]

    def translatePushThis(self, constant):
        '''

        :param constant: integer
        :return:
        '''
        return ["@" + str(constant),
                "D=A",
                "@THIS",
                "A=M",
                "A=A+D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"]


    def translatePushTemp(self, constant):
        return ["@" + str(5 + constant),
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"]

    def translatePushArgument(self, constant):
        '''

        :param constant: integer
        :return:
        '''
        return ["@" + str(constant),
                "D=A",
                "@ARG",
                "A=M",
                "A=A+D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"]

    def translatePushLocal(self, constant):
        '''

        :param constant: integer
        :return:
        '''
        return ["@" + str(constant),
                "D=A",
                "@LCL",
                "A=M",
                "A=A+D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"]

    def translatePushPointer(self, constant):
        '''

        :param constant: integer
        :return:
        '''

        return ["@" + str(3 + constant),
                "A=M",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"]

    def translatePushConstant(self, constant):
        '''
        Return assembly code for a push constant VM instruction
        :param constant: integer constant
        :return:
        '''

        return ["@" + str(constant), "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]


    def translatePushStatic(self, constant):
        '''

        :param constant: integer
        :return:
        '''
        return ["@" + str(constant),
                "D=A",
                "@" + self.currentVMFile + "." + str(constant),
                "A=M",
                "A=A+D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"]

    def translatePop(self, command):
        '''
        Todo: this, that, pointer, etc aren't directly mapped to RAM 0-5, you need to use
        the values as a pointer to the actual memory segment
        :param command:
        :return:
        '''
        self.parser.setInstruction(command)

        label = self.parser.arg1()
        offset = int(self.parser.arg2())

        if label == "local":
            return self.translatePopLocal(offset)
        elif label == "argument":
            return self.translatePopArgument(offset)
        elif label == "pointer":
            return self.translatePopPointer(offset)
        elif label == "static":
            return self.translatePopStatic(offset)
        elif label == "temp":
            return self.translatePopTemp(offset)
        elif label == "this":
            return self.translatePopThis(offset)
        elif label == "that":
            return self.translatePopThat(offset)







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