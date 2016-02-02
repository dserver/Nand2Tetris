// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// initialization. 
@i
M=0 // i = 0. stop when i equals r1
@R2
M=0 // initialize sum to 0

// check if loop has gone R1 times yet
(loop)
@R1
D=M // store R1 in D
@i
D=D-M // store i - R1 in D
@end
D;JEQ // if zero, we're done


// Add R0 to R2
@R0
D=M
@R2
M=D+M // M[sum] += R0

// need to increment i here...
@i
M=M+1

@loop 
0;JMP // jump back to start of loop

(end)

@end
0; JMP