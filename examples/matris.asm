EQU matris #0x1000
EQU matris2 #0x1010

B write_OROS
main:
    MOV r1, $matris
    mov r2, #0b0000001111000000
    STR r2, [r1,#2]
    mov r2, #0b0000011111100000
    STR r2, [r1,#3]
    mov r2, #0b0000111111110000
    STR r2, [r1,#4]
    mov r2, #0b0001111111111000
    STR r2, [r1,#5]
    mov r2, #0b0011111111111100
    STR r2, [r1,#6]
    mov r2, #0b0111111111111110
    STR r2, [r1,#7]
    STR r2, [r1,#8]
    STR r2, [r1,#9]
    STR r2, [r1,#10]
    STR r2, [r1,#11]
    mov r2, #0b0111111001111110
    STR r2, [r1,#12]
    mov r2, #0b0011111001111100
    STR r2, [r1,#13]
stop:
    B stop

write_NIDOS:
    MOV r1, $matris2
    ADD r1, r1, #1
    BL write_N
    ADD r1, r1, #3
    BL write_I
    ADD r1, r1, #2
    BL write_D
    ADD r1, r1, #3
    BL write_O
    ADD r1, r1, #3
    BL write_S
    B main

write_OROS:
    MOV r1, $matris2
    ADD r1, r1, #1
    BL write_O
    ADD r1, r1, #3
    BL write_R
    ADD r1, r1, #3
    BL write_O
    ADD r1, r1, #3
    BL write_S
    B main

write_D:
    mov r2, #0b1111111010000010
    STR r2, [r1]
    mov r2, #0b1000001001111100
    STR r2, [r1, #1]
    BX

write_N:
    mov r2, #0b1111111000100000
    STR r2, [r1]
    mov r2, #0b0001000011111110
    STR r2, [r1,#1]
    BX

write_I:
    mov r2, #0b1000001011111110
    STR r2, [r1]
    mov r2, #0b1000001000000000
    STR r2, [r1, #1]
    BX

write_O:
    mov r2, #0b0111110010000010
    STR r2, [r1]
    mov r2, #0b1000001001111100
    STR r2, [r1, #1]
    BX

write_S:
    mov r2, #0b0110010010010010
    STR r2, [r1]
    mov r2, #0b1001001001001100
    STR r2, [r1, #1]
    BX

write_A:
    mov r2, #0b0111111010001000
    STR r2, [r1]
    mov r2, #0b1000100001111110
    STR r2, [r1,#1]
    BX

write_R:
    mov r2, #0b1111111010010000
    STR r2, [r1]
    mov r2, #0b1001000001101110
    STR r2, [r1,#1]
    BX

write_R:
    mov r2, #0b1111111010010000
    STR r2, [r1]
    mov r2, #0b1001000001101110
    STR r2, [r1,#1]
    BX

write_E:
    mov r2, #0b1111111010010010
    STR r2, [r1]
    mov r2, #0b1001001010000010
    STR r2, [r1,#1]
    BX

write_V:
    mov r2, #0b1111100000000110
    STR r2, [r1]
    mov r2, #0b0000011011111000
    STR r2, [r1,#1]
    BX

write_Y:
    mov r2, #0b1110010000010010
    STR r2, [r1]
    mov r2, #0b0001001011111100
    STR r2, [r1,#1]
    BX

write_U:
    mov r2, #0b1111110000000010
    STR r2, [r1]
    mov r2, #0b0000001011111100
    STR r2, [r1,#1]
    BX

write_C:
    mov r2, #0b0111110010000010
    STR r2, [r1]
    mov r2, #0b1000001001000100
    STR r2, [r1,#1]
    BX