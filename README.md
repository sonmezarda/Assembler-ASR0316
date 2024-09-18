## ASR0316 Assembly language to hex/bin converter.

#### ASR0316 is a Microprocessor project with 16-bit architecture and 32-bit (thanks to Harvard architecture) Instructions.
#### I aimed to make it similar to an ARM-based instruction set.

```
EQU screen #0xFFFC // EQU can be used to define constant
EQU color #0xe053 // The # symbol is used for numeric values 
// numeric values can be hex, binary or decimal ( #0xABCD, 0b00100111, #58 )
// all numerics must be between 0 - 65565

MOV r1, $screen // The $ prefix is used to denote constants.
MOV r2, #2
STR r2, [r1, #3] // [rx, #numeric] Can be used for address shifting
MOV r3, $color
STR r3, [r1, #2]
MOV r5, #0
MOV r4, #1

mloop: // Label lines must be end with ':' char.
    MOV r2, #0
    STR r5, [r1, #1]
    STR r3, [r1, #2]
loop:
    STR r2, [r1] // [rx] symbol is used to use the specified register as the address.
    STR r4, [r1, #3]
    ADD r2, r2, #1
    CMP r2, #66
    BNE loop
    ADD r5, r5, #1
    CMP r5, #66 //CMP is used to compare registers and set flags. Also, set-flag can be set with uses such as ADDS, SUBS.
    BNE mloop
```
