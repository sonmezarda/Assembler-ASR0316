EQU button #0xFFFF
EQU screen #0x0000
EQU squareSize #128

MOV r0, r0
MOV r2, $button
MOV r0, $screen // r0 = screen reg
MOV r7, #1 // r7 = control reg
bloop:
    LDR r1, [r2]
    SUBS r1, r1, #1
    BNE setBlack

setWhite:
    MOV r3, #0
    STR r3, [r0, #2]
    B drawSquare

setBlack:
    MOV r3, #1
    STR r3, [r0, #2]
    B drawSquare

drawSquare:
    MOV r5, $squareSize // r5 = col reg
    MOV r6, $squareSize // r6 = row reg
    loop:
        SUBS r5, r5, #1 // decrement col
        STR r5, [r0] // set col
        STR r7, [r0, #3] // set control
        BNE loop
        SUBS r6, r6, #1 // decrement row
        STR r6, [r0, #1] // set row
        MOV r5, $squareSize // reset col
        BNE loop // loop

B bloop // loop