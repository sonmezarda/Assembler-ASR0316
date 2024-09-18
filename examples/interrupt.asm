EQU int #0x0000

MOV r1, $int
MOV r2, #15
STR r2, [r1, #1]
MOV r2, #0x00FF
STR r2, [r1, #4]

