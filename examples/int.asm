EQU screen #0xFFFC
EQU clr #0x8fc4
EQU int #0x0001

mov r1, $int
mov r6, button
STR r6, [r1]
MOV r1, $screen
MOV r2, #2
STR r2, [r1, #3]
MOV r3, $clr
STR r3, [r1, #2]
MOV r2, #0
MOV r4, #1
button:
CMP r1, r1
ADD r5, r5, #1
STR r5, [r1, #1]
loop:
STR r2, [r1]
STR r4, [r1, #3]
ADD r2, r2, #1
B loop