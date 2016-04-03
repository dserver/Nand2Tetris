    @SP
    M=M-1
    A=M
    D=M // D is arg1
    @SP
    M=M-1
    A=M
    D=D-M // M is arg2
    @EQUAL
    D;JEQ
    @NOTEQUAL
    0;JEQ

(EQUAL)
    @SP
    A=M
    M=0
    @CONTINUE
    0;JEQ

(NOTEQUAL)
    @SP
    A=M
    M=-1

(CONTINUE)
@SP
M=M+1 // finally, increment SP