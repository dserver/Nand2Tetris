from VirtualMachine.Parser import Parser

class CodeWriter:


    def __init__(self, parser):
        '''
        Opens the output file and gets ready to write into it
        :param parser object to use
        :return:
        '''
        self.parser = Parser()
        self.eqCounter = 0

    def setFileName(self, fileName):
        '''
        Changes VM file that is currently being translated
        :param fileName:
        :return:
        '''
        pass

    def translateArithmetic(self, command):
        '''
        Writes the assembly code that is the translation of the given
        arithmetic command
        :param command: command string
        :return: list where each element is one line of assembly code
        '''
        self.parser.setInstruction(command)
        if self.parser.currentInstructionType != self.parser.C_ARITHMETIC:
            raise RuntimeError("translate arithmetic cannot translate non-arithmetic type")

        if command == "add":
            return ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=D+M",
                             "@SP", "M=M+1"]
        elif command == "eq":
            self.eqCounter += 1
            return ['@SP', 'M=M-1', 'A=M', 'D=M', '@SP', 'M=M-1', 'A=M', 'D=D-M', '@EQUAL' + str(self.eqCounter), 'D;JEQ', '@NOTEQUAL' + str(self.eqCounter), '0;JEQ',
                     '(EQUAL' + str(self.eqCounter) + ')', '@SP', 'A=M', 'M=0', '@CONTINUE'  + str(self.eqCounter),
                                '0;JEQ', '(NOTEQUAL' + str(self.eqCounter) + ')', '@SP', 'A=M', 'M=-1',
                     '(CONTINUE' + str(self.eqCounter) + ')', '@SP', 'M=M+1']

    def writePushPop(self, command):
        '''
        Writes the assembly code that is a translation of the command
        Only called when command is either C_PUSH or C_POP
        :param command:
        :return:
        '''
        pass

    def close(self):
        '''
        Close output file
        :return:
        '''
        pass