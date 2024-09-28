equ ioAddr #0x2000

mov r0, r0
mov r0, $ioAddr
mov r1, #0xF0FF

readLoop:
    str r1, [r0]
    b readLoop
end:
    b end