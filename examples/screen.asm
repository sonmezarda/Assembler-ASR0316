EQU screen #0xFFFC
EQU color #0xe053

MOV r1, $screen
MOV r2, #2
STR r2, [r1, #3]
MOV r3, $color
STR r3, [r1, #2]
MOV r5, #0
MOV r4, #1
// comment test
mloop:
    MOV r2, #0
    STR r5, [r1, #1]
    STR r3, [r1, #2]
loop:
    STR r2, [r1]
    STR r4, [r1, #3]
    ADD r2, r2, #1
    CMP r2, #66
    BNE loop
    ADD r5, r5, #1
    CMP r5, #66
    BNE mloop