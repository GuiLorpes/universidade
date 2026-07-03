.globl main

.section .data
    n1 : .int 2
    n2 : .int 3

.section .bss
    resultado : .int

.section .text
    main:
        movl n1, %eax
        movl n2, %ebx
        addl %eax, %ebx
        movl %ebx, resultado
        movl $1, %eax
        movl resultado, %ebx
        int $0x80

