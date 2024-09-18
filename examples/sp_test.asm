MOV r13, #0x0010

main:
    mov r2, #0xFFAA
    BL test
    MOV r3, #0xAABB
    B end

test:
    push r14 
    mov r1, #0xFFFF
    BL t2st
    pop r14
    BX

t2st:
    mov r4, #0x1234
    BX

end:
    B end