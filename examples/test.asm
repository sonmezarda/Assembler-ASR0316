EQU screen #0x0000
EQU color #1
EQU squareSize #127
MOV r1, $screen
MOV r2, $squareSize // col reg
MOV r5, $squareSize // row reg
MOV r4, #1 // control reg

MOV r3, $color // color reg
STR r3, [r1, #2] // set color

loop:
    STR r2, [r1] // set col
    STR r4, [r1, #3] // set control
    SUBS r2, r2, #1 // increment col
    BNE loop
    SUBS r5, r5, #1 // increment row
    STR r5, [r1, #1] // set row
    MOV r2, $squareSize // reset col
    BNE loop // loop

end:
    B end


