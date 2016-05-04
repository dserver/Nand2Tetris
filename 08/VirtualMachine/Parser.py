
class Parser:

    def __init__(self):
        self.C_ARITHMETIC = 0
        self.C_PUSH = 1
        self.C_POP = 2
        self.C_LABEL = 3
        self.C_GOTO = 4
        self.C_IF = 5
        self.C_FUNCTION = 6
        self.C_RETURN = 7
        self.C_CALL = 8

        self.ArithmeticCommands = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        self.currentInstructionType = None
        self.currentInstruction = None

    def setInstruction(self, command):
        '''
        Set the current instruction for the Parser
        :param command: string command
        :return:
        '''
        self.currentInstructionType = self.commandType(command)
        self.currentInstruction = command

    def commandType(self, command):
        '''
        Parse the command to figure out what type of command it is
        :param command:
        :return: Parser.C_TYPE (see init)
        '''
        splitCommand = command.split()
        if len(splitCommand) == 1:
            if splitCommand[0] in self.ArithmeticCommands:
                return self.C_ARITHMETIC
            elif splitCommand[0] == 'return':
                return self.C_RETURN
            else:
                raise RuntimeError("Invalid 0 arg command")

        elif len(splitCommand) == 2:
            if (splitCommand[0] == 'goto'):
                return self.C_GOTO
            elif splitCommand[0] == 'if-goto':
                return self.C_IF
            elif splitCommand[0] == 'label':
                return self.C_LABEL
            else:
                raise RuntimeError("Invalid 1 arg command")

        elif len(splitCommand) == 3:
            if splitCommand[0] == 'push':
                return self.C_PUSH
            elif splitCommand[0] == 'pop':
                return self.C_POP
            elif splitCommand[0] == "function":
                return self.C_FUNCTION
            elif splitCommand[0] == "call":
                return self.C_CALL
            else:
                raise RuntimeError("Invalid 2 arg command")

    def arg0(self):
        return self.currentInstruction.split()[0]

    def arg1(self):
        '''
        Return the first argument for commands that have at least 1 arg
        :return: arg1
        '''
        if self.currentInstructionType in [self.C_POP, self.C_PUSH, self.C_LABEL, self.C_FUNCTION,
                                           self.C_GOTO, self.C_FUNCTION, self.C_CALL, self.C_IF]:
            split = self.currentInstruction.split()
            return split[1]
        else:
            raise RuntimeError("Invalid call to arg1. Type not C_ARITHMETIC but " + str(self.currentInstructionType))

    def arg2(self):
        '''
        Return the second argument for commands that have at least 1 arg
        :return: arg1
        '''
        if self.currentInstructionType in [self.C_POP, self.C_PUSH, self.C_FUNCTION,
                                           self.C_FUNCTION, self.C_CALL]:
            split = self.currentInstruction.split()
            return split[2]
        else:
            raise RuntimeError("Invalid call to arg1. Type not C_ARITHMETIC but " + str(self.currentInstructionType))

