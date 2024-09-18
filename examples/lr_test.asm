main:
    MOV r1, #0x0002
loop:
    SUB r1, r1, #1
    CMP r1, #0
    BNE loop
    BL test
    MOV r3, #0xFEAD
test:
    MOV r2, #0xDEAD
    BX