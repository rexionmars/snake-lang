#!/usr/bin/env python3

import sys
import subprocess

iota_counter = 0

def iota(reset = False):
    global iota_counter

    if reset:
        iota_counter = 0

    result = iota_counter
    iota_counter += 1

    return result

OP_PUSH = iota(True)
OP_PLUS = iota()
OP_MINUS = iota()
OP_DUMP = iota()
COUNT_OPS = iota()

def push(x):
    return (OP_PUSH, x)

def plus() -> tuple:
    return (OP_PLUS, )

def minus() -> tuple:
    return (OP_MINUS, )

def dump() -> tuple:
    return (OP_DUMP, )

def simulate_program(program):
    stack = []

    for operation in program:
        assert COUNT_OPS == 4, 'Exhaustive handling of operations in simulation'

        if operation[0] == OP_PUSH:
            stack.append(operation[1])

        elif operation[0] == OP_PLUS:
            x = stack.pop()
            y = stack.pop()
            stack.append(x + y)

        elif operation[0] == OP_MINUS:
            x = stack.pop()
            y = stack.pop()
            stack.append(y - x)

        elif operation[0] == OP_DUMP:
            x = stack.pop()
            print(x)

        else:
            assert False, 'unreachable'

def compile_program(program, out_file_path):
    # Hardcode injection code in assembly
    with open(out_file_path, "w") as out:
        out.write('segment .text\n')
        out.write(f'dump(unsigned long):\n')
        out.write(f'    push    rbp\n')
        out.write(f'    mov     rbp, rsp\n')
        out.write(f'    sub     rsp, 64\n')
        out.write(f'    mov     QWORD PTR [rbp-56], rdi\n')
        out.write(f'    mov     QWORD PTR [rbp-8], 1\n')
        out.write(f'    mov     eax, 32\n')
        out.write(f'    sub     rax, QWORD PTR [rbp-8]\n')
        out.write(f'    mov     BYTE PTR [rbp-48+rax], 10\n')
        out.write(f'.L2:\n')
        out.write(f'    mov     rcx, QWORD PTR [rbp-56]\n')
        out.write(f'    movabs  rdx, -3689348814741910323\n')
        out.write(f'    mov     rax, rcx\n')
        out.write(f'    mul     rdx\n')
        out.write(f'    shr     rdx, 3\n')
        out.write(f'    mov     rax, rdx\n')
        out.write(f'    sal     rax, 2\n')
        out.write(f'    add     rax, rdx\n')
        out.write(f'    add     rax, rax\n')
        out.write(f'    sub     rcx, rax\n')
        out.write(f'    mov     rdx, rcx\n')
        out.write(f'    mov     eax, edx\n')
        out.write(f'    lea     edx, [rax+48]\n')
        out.write(f'    mov     eax, 31\n')
        out.write(f'    sub     rax, QWORD PTR [rbp-8]\n')
        out.write(f'    mov     BYTE PTR [rbp-48+rax], dl\n')
        out.write(f'    add     QWORD PTR [rbp-8], 1\n')
        out.write(f'    mov     rax, QWORD PTR [rbp-56]\n')
        out.write(f'    movabs  rdx, -3689348814741910323\n')
        out.write(f'    mul     rdx\n')
        out.write(f'    mov     rax, rdx\n')
        out.write(f'    shr     rax, 3\n')
        out.write(f'    mov     QWORD PTR [rbp-56], rax\n')
        out.write(f'    cmp     QWORD PTR [rbp-56], 0\n')
        out.write(f'    jne     .L2\n')
        out.write(f'    mov     eax, 32\n')
        out.write(f'    sub     rax, QWORD PTR [rbp-8]\n')
        out.write(f'    lea     rdx, [rbp-48]\n')
        out.write(f'    lea     rcx, [rdx+rax]\n')
        out.write(f'    mov     rax, QWORD PTR [rbp-8]\n')
        out.write(f'    mov     rdx, rax\n')
        out.write(f'    mov     rsi, rcx\n')
        out.write(f'    mov     edi, 1\n')
        out.write(f'    call    write\n')
        out.write(f'    nop\n')
        out.write(f'    leave\n')
        out.write(f'    ret\n')
        out.write('global _start\n')
        out.write('_start:\n')

        for operation in program:
            assert COUNT_OPS == 4, 'Exhaustive handling of operations in compilation'
            if operation[0] == OP_PUSH:
                out.write(f'    ;;-- push {operation[1]} --\n')
                out.write(f'    push {operation[1]}\n')

            elif operation[0] == OP_PLUS:
                out.write('    ;;-- plus --\n')
                out.write('    pop rax\n')
                out.write('    pop rbx\n')
                out.write('    add rax, rbx\n')
                out.write('    push rax\n')
            elif operation[0] == OP_MINUS:
                out.write('    ;;-- minus --\n')
                out.write('    pop rax\n')
                out.write('    pop rbx\n')
                out.write('    sub rax, rbx\n')
                out.write('    push rax\n')
            elif operation[0] == OP_DUMP:
                out.write('    ;; -- dump --\n')
                out.write('    pop rdi\n')
                out.write('    call dump\n')

            else:
                assert False, 'unreachable'

        out.write('    mov rax, 60\n')
        out.write('    mov rdi, 0\n')
        out.write('    syscall\n')

# Unhardcode program
program = [
    push(34),
    push(35),
    plus(),
    dump(),
    push(500),
    push(80),
    minus(),
    dump(),
]

def usage_mode():
    """Usage: snake <SUBCOMMAND> <ARGS>

    SUBCOMMANDS:
    test            Simulate the program
    compile         Compile the program
    """

def call_subcmd(cmd):
    print(f'runnig -> {cmd}')
    subprocess.call(cmd)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(usage_mode.__doc__)
        print('ERROR: it is necessary to supply a subcommand')
        exit(1)

    subcommand = sys.argv[1]

    if subcommand == 'test':
        simulate_program(program)

    elif subcommand == 'compile':
        compile_program(program, 'test/test.asm')
        call_subcmd(['nasm', '-felf64', 'test/test.asm'])
        call_subcmd(['ld', '-o', 'test/output', 'test/test.o'])

    else:
        print(usage_mode.__doc__)
        print(f'\nERROR!: unknown subcommand: \"{subcommand}\"')
        exit(1)