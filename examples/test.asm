MOV r1, #0
loop:
    ADD r1, r1, #1
    STR r1, [0x000F]
    B loop  