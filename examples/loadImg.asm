EQU screen #0xFFFC
EQU color #0xe053

MOV r13, #0x3ff8

MOV r1, $screen
MOV r2, #2
STR r2, [r1, #3]
MOV r3, $color
STR r3, [r1, #2]
MOV r4, #1
MOV r5, #64
MOV r6, #0
mloop:
    MOV r2, #64
    SUB r5, r5, #1
    STR r5, [r1, #1]
    
loop:
    SUB r2, r2, #1
    LDR r3, [r6]
    STR r3, [r1, #2]
    STR r2, [r1]
    STR r4, [r1, #3]
    ADD r6, r6, #1
    CMP r2, #0
    BNE loop
    CMP r5, #0
    BNE mloop

end:
    B end