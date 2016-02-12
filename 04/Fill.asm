// Author: Jonathan Henk
// Second assignment in Chapter 4 of
// The Elements of Computing Systems


// Paint screen black if key is pressed. If
// no key is pressed paint screen white.


(START)
@KBD
D=M // D = key pressed
@PAINTBLACK
D;JGT // if d > 0: paint black
@PAINTWHITE
0;JEQ // if d == 0: paint white


(PAINTBLACK)
@i
M=0 // i = 0

(LOOPB)
@SCREEN
D=A // D = SCREEN
@i
A=D+M // A = SCREEN + i
D=-1
M=D // RAM[D] = 0xFFFF


@i
M=M+1 // i++
D=M   // D = i
@8192 // number of cells in screen
D=A-D
@START
D;JEQ // go back to start
@LOOPB
0;JEQ // go back to loopB (keep painting black)



(PAINTWHITE)
@i
M=0 // i = 0

(LOOPW)
@SCREEN
D=A // D = SCREEN
@i
A=D+M // A = SCREEN + i
M=0 // RAM[D] = 0x0000


@i
M=M+1 // i++
D=M   // D = i
@8192 // number of cells in screen
D=A-D
@START
D;JEQ // go back to start
@LOOPW
0;JEQ // go back to loopB (keep painting white)