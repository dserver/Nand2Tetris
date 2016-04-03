
Command Types:
    C_Arithmetic
    C_Push, C_Pop
    C_Label
    C_Goto, C_If
    C_Function
    C_Return
    C_Call


// Put RAM[ RAM[xxx] + offset ] into A/D, then push onto stack
// Example: push local 2. local equals some value, say 12 (static RAM)
    @xxx
    A=M
    D=A
    @offset
    A=D+A
    A/D=M
    @SP // Push A/D on stack
    A=M
    M=A/D
    @SP
    M=M+1 // Increment stack pointer

// Push D on to stack
    @SP
    A=M
    M=D


// Add
    @SP
    M=M-1
    A=M
    D=M // D is arg1
    @SP
    M=M-1
    A=M
    M=D+M // M is arg2
    @SP
    M=M+1 // increment stack pointer

// Subtract
    @SP
    M=M-1
    A=M
    D=M // D is arg1
    @SP
    M=M-1
    A=M
    M=D-M // M is arg2
    @SP
    M=M+1 // increment stack pointer

// Equal
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
