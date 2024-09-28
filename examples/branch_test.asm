nop

mov r1, #0

CMP r1, #0

BEQ true

false:
    MOV r2, #0x3333
    B end

true:
    MOV r2, #0x4444
    B end


end:
    B end
