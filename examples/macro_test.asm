nop 

mov r1, #1
mov r2, #2
mov r3, #3
mov r4, #4

push {r1, r2, r3, r4}
mov r1, #0
mov r2, #0
mov r3, #0
mov r4, #0
pop {r1, r2, r3, r4}

end:
    b end