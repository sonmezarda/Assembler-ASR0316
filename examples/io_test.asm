equ ioAddr #0x1000

mov r0, r0
mov r0, $ioAddr

readLoop:
    ldr r1, [r0]
    adds r1, r1, #0
    BEQ readLoop
    mov r2, r1
    b readLoop
end:
b end