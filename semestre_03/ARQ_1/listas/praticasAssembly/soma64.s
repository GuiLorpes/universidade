.globl main

.section .data
    n1 : .quad 2
    n2 : .quad 3

.section .bss
    resultado : .quad

.section .text
    main:
        movq n1, %rax
        movq n2, %rbx
        addq %rax, %rbx
        movq %rbx, resultado
        movq $60, %rax
        movq resultado, %rdi
        syscall
