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
        self.callerCounter = 0 # same as eqCounter but for return address labels
        self.memoryMappedRegisters = {"local": "LCL",
                       "argument": "ARG",
                       "this": "R3",
                       "that": "R4",
                       "pointer": "R3",
                        "temp": "R5"}

        self.currentVMFile = ""
        self.file = None
        self.currentFunction = ""





    def setCurrentVMFile(self, fileName):
        '''
        Changes VM file that is currently being translated
        :param fileName:
        :return:
        '''
        self.currentVMFile = fileName[:-3]

    def setCurrentFunction(self, function):
        '''
        Set function scope to what is being compiled. Used for label, if-goto, goto, etc.
        :param function:
        :return:
        '''

        self.currentFunction = function



    def assembleVMCommand(self, command):
        self.parser.setInstruction(command)
        if self.parser.commandType(command) == self.parser.C_ARITHMETIC:
            return self.translateArithmetic(command)


        elif self.parser.commandType(command) in [self.parser.C_PUSH, self.parser.C_POP]:
            return self.translatePushPop(command)


        elif self.parser.commandType(command) == self.parser.C_FUNCTION:
            return self.translateFunction(self.parser.arg2())


        elif self.parser.commandType(command) == self.parser.C_CALL:
            return self.translateCall(self.parser.arg1(), int(self.parser.arg2()))


        elif self.parser.commandType(command) == self.parser.C_RETURN:
            return self.translateReturn()


        elif self.parser.commandType(command) == self.parser.C_LABEL:
            return self.translateLabel(self.parser.arg1())


        elif self.parser.commandType(command) == self.parser.C_IF:
            return self.translateIfGoto(self.parser.arg1())


        elif self.parser.commandType(command) == self.parser.C_GOTO:
            return self.translateGoto(self.parser.arg1())





    def translateArithmetic(self, command):
        '''
        Writes the assembly code that is the translation of the given
        arithmetic command
        :param command: command string
        :return: list where each element is one line of assembly code

        :todo "sub", "neg", "gt", "lt", "and", "or", "not"]
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
            return ["@SP", "A=M", "A=A-1", "M=!M"]
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



    def translateLabel(self, label):
        return ["(" + self.currentFunction + "$" + label + ")"]



    def translateGoto(self, label):
        return ["@" + self.currentFunction + "$" + label,
                "0;JEQ"]


    def translateIfGoto(self, label):
        return ["@SP",
                "M=M-1",
                "@SP",
                "A=M",
                "D=M",
                "@" + self.currentFunction + "$" + label,
                "D;JNE"]


    def translateFunction(self, function):
        '''
        Assembly instructions with comments to implement function
        declaration

        (FileName.Function)
        @LCL
        A=M
        M=0 // set first local variable to 0
        @LCL
        A=M
        A=A+1
        M=0 // set every other local variable to 0. do (nlocal-1) times

        :param function:
        :param nargs:
        :return:
        '''
        asm = ["(" + self.currentVMFile + "." + function + ")",
               "@SP"]

        nargs = int(self.parser.arg2())

        for i in xrange(0, nargs):
            asm.append("M=M+1")

        return asm

    def translateReturn(self):
        '''

        Assembly instructions with comments  to implement return

        @SP // SP is sitting at the end of the global stack
        A=M-1
        D=M // D is return value
        @ARG
        A=M
        M=D // return value replaces arg0 at top of stack

        @LCL
        A=M-1
        D=M // D holds address of caller THAT on frame
        @THAT
        M=D // restores caller's THAT at RAM start

        @LCL
        A=M-1
        A=A-1
        D=M // D holds callers THIS
        @THIS
        M=D // restores callers THIS

        // Restores callers stack pointer
        @ARG
        D=M+1 // D holds first address in callee's frame + 1
        @SP
        M=D // restores caller's stack pointer to one after return value

        // restores callers ARG
        @LCL
        A=M-1
        A=A-1
        A=A-1
        D=M // D holds callers ARG
        @ARG
        M=D // restores callers ARG

        // Save Callee LCL for easy access to return address
        @LCL
        A=M
        D=M
        @R8
        M=D // callee LCL stored in R8

        // Restore callers LCL
        @LCL
        A=M-1
        A=A-1
        A=A-1
        A=A-1
        D=M // D holds callers LCL
        @LCL
        M=D // restores callers LCL

        // Return to caller
        @R8
        A=M-1
        A=A-1
        A=A-1
        A=A-1
        A=A-1
        A=M // A holds return address
        0;JEQ // return to caller

        :return:
        '''

        return ["@SP",
                "A=M-1",
                "D=M",
                "@ARG",
                "A=M",
                "M=D",
                "@LCL",
                "A=M-1 ",
                "D=M",
                "@THAT",
                "M=D",
                "@LCL",
                "A=M-1",
                "A=A-1",
                "D=M",
                "@THIS",
                "M=D",
                "@ARG",
                "D=M+1",
                "@SP",
                "M=D",
                "@LCL",
                "A=M-1",
                "A=A-1",
                "A=A-1",
                "D=M",
                "@ARG",
                "M=D",
                "@LCL",
                "D=M",
                "@R8",
                "M=D",
                "@LCL",
                "A=M-1",
                "A=A-1",
                "A=A-1",
                "A=A-1",
                "D=M",
                "@LCL",
                "M=D",
                "@R8",
                "A=M-1",
                "A=A-1",
                "A=A-1",
                "A=A-1",
                "A=A-1",
                "A=M",
                "0;JEQ"]


    def translateCall(self, function, nargs):
        '''

        Below is assembly implementation of "call function nargs"

            // arg's already pushed on stack
            @CurrentFunction.Callee1
            D=A
            @SP
            A=M
            M=D // push return address on top of stack

            @SP
            M=M+1 // increment SP

            @LCL
            D=M
            @SP
            A=M
            M=D // push callee LCL

            @SP
            M=M+1 // increment SP

            @ARG
            D=M
            @SP
            A=M
            M=D // push callee ARG

            @SP
            M=M+1 // increment SP

            @THIS
            D=M
            @SP
            A=M
            M=D // push callee THIS

            @SP
            M=M+1 // increment SP

            @THAT
            D=M
            @SP
            A=M
            M=D // push callee THAT

            @SP
            M=M+1 // increment SP

            @5+nargs // set callee ARG to top of arg stack
            D=A
            @SP
            D=A-D
            @ARG
            M=D

            @SP
            D=A
            @LCL
            M=D // set callee LCL to local segment

            @CalledFunction // jump to called function
            0;JEQ

            (CurrentFunction.Callee1) // return address

        :param function: string
        :param nargs: integer
        :return:
        '''

        self.callerCounter += 1

        return ["@Callee" + str(self.callerCounter),
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                "@LCL",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                "@ARG",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                "@THIS",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                "@THAT",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                "@"+str(5+nargs),
                "D=A",
                "@SP",
                "D=A-D",
                "@ARG",
                "M=D",
                "@SP",
                "D=A",
                "@LCL",
                "M=D",
                "@CalledFunction",
                "0;JEQ",
                "(Callee" + str(self.callerCounter) + ")"]


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