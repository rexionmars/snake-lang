#!/usr/bin/env python3

import sys
import shlex
import subprocess

from os import path

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
colorama_init()

iota_counter = 0
def iota(reset = False):
    global iota_counter

    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result

# Common operations in stack
OP_PUSH = iota(True)
OP_PLUS = iota()
OP_MINUS = iota()
OP_EQUAL = iota()
OP_DUMP = iota()
OP_IF = iota()
OP_ELSE = iota()
OP_END = iota()

# Count operations in stack
COUNT_OPS = iota()
print(f'OPERATIONS IN STACK: [{Fore.RED}{COUNT_OPS}{Style.RESET_ALL}]')

# Common operations declarations
push = lambda x: (OP_PUSH, x)
plus = lambda: (OP_PLUS, )
minus = lambda: (OP_MINUS, )
equal = lambda: (OP_EQUAL, )
dump = lambda: (OP_DUMP, )
if_block = lambda: (OP_IF, )
else_op = lambda: (OP_ELSE, )
end_block_code = lambda: (OP_END, )

# Simulate the program without compiler 
def simulate_program(program):
    stack = []
    addr = 0

    while addr < len(program):
        assert COUNT_OPS == 8, 'Exhaustive handling of operations in simulation'
        operation = program[addr]

        if operation[0] == OP_PUSH:
            stack.append(operation[1])
            addr += 1
        elif operation[0] == OP_PLUS:
            x = stack.pop()
            y = stack.pop()
            stack.append(x + y)
            addr += 1
        elif operation[0] == OP_MINUS:
            x = stack.pop()
            y = stack.pop()
            stack.append(y - x)
            addr += 1
        elif operation[0] == OP_EQUAL:
            x = stack.pop()
            y = stack.pop()
            stack.append(int(x == y)) # 1 = True, 0 = False -- Default return is True or False
            addr += 1
        elif operation[0] == OP_IF:
            x = stack.pop()
            if x == 0:
                assert len(operation) >= 2, f'{Fore.RED}`if`{Style.RESET_ALL} instruction does not '+\
                f'have a reference to the end its block. Please call {Fore.YELLOW}cross_reference_blocks(){Style.RESET_ALL}'
                addr = operation[1]
            else:
                addr += 1
        elif operation[0] == OP_ELSE:
            assert len(operation) >= 2, f'{Fore.RED}`if`{Style.RESET_ALL} instruction does not '+\
            f'have a reference to the end its block. Please call {Fore.YELLOW}cross_reference_blocks(){Style.RESET_ALL}'
            addr = operation[1]
        elif operation[0] == OP_END:
            addr += 1
        elif operation[0] == OP_DUMP:
            x = stack.pop()
            print(x)
            addr += 1
        else:
            assert False, 'unreachable'

# Compile the program for machine code
def compile_program(program, out_file_path):
    # Hardcode Dump function, So is temporary
    with open(out_file_path, 'w') as out:
        out.write('BITS 64\n')
        out.write('segment .text\n')
        out.write('dump:\n')
        out.write('    push    rbp\n')
        out.write('    mov     rbp, rsp\n')
        out.write('    sub     rsp, 64\n')
        out.write('    mov     QWORD [rbp-56], rdi\n')
        out.write('    mov     QWORD [rbp-8], 1\n')
        out.write('    mov     eax, 32\n')
        out.write('    sub     rax, QWORD [rbp-8]\n')
        out.write('    mov     BYTE  [rbp-48+rax], 10\n')
        out.write('.L2:\n')
        out.write('    mov     rcx, QWORD [rbp-56]\n')
        out.write('    mov     rdx, -3689348814741910323\n')
        out.write('    mov     rax, rcx\n')
        out.write('    mul     rdx\n')
        out.write('    shr     rdx, 3\n')
        out.write('    mov     rax, rdx\n')
        out.write('    sal     rax, 2\n')
        out.write('    add     rax, rdx\n')
        out.write('    add     rax, rax\n')
        out.write('    sub     rcx, rax\n')
        out.write('    mov     rdx, rcx\n')
        out.write('    mov     eax, edx\n')
        out.write('    lea     edx, [rax+48]\n')
        out.write('    mov     eax, 31\n')
        out.write('    sub     rax, QWORD [rbp-8]\n')
        out.write('    mov     BYTE  [rbp-48+rax], dl\n')
        out.write('    add     QWORD  [rbp-8], 1\n')
        out.write('    mov     rax, QWORD [rbp-56]\n')
        out.write('    mov     rdx, -3689348814741910323\n')
        out.write('    mul     rdx\n')
        out.write('    mov     rax, rdx\n')
        out.write('    shr     rax, 3\n')
        out.write('    mov     QWORD [rbp-56], rax\n')
        out.write('    cmp     QWORD [rbp-56], 0\n')
        out.write('    jne     .L2\n')
        out.write('    mov     eax, 32\n')
        out.write('    sub     rax, QWORD [rbp-8]\n')
        out.write('    lea     rdx, [rbp-48]\n')
        out.write('    lea     rcx, [rdx+rax]\n')
        out.write('    mov     rax, QWORD [rbp-8]\n')
        out.write('    mov     rdx, rax\n')
        out.write('    mov     rsi, rcx\n')
        out.write('    mov     edi, 1\n')
        out.write('    mov     rax, 1\n')
        out.write('    syscall\n')
        out.write('nop\n')
        out.write('leave\n')
        out.write('ret\n')
        out.write('global _start\n')
        out.write('_start:\n')

        # Translate the program for machine code
        for addr in range(len(program)):
            operation = program[addr]
            assert COUNT_OPS == 8, 'Exhaustive handling of operations in compilation'
            if operation[0] == OP_PUSH:
                out.write(f'   ; -- push {operation[1]} --\n')
                out.write(f'   push {operation[1]}\n')

            elif operation[0] == OP_PLUS:
                out.write('    ; -- plus --\n')
                out.write('    pop rax\n')
                out.write('    pop rbx\n')
                out.write('    add rax, rbx\n')
                out.write('    push rax\n')
            elif operation[0] == OP_MINUS:
                out.write('    ; -- minus --\n')
                out.write('    pop rax\n')
                out.write('    pop rbx\n')
                out.write('    sub rbx, rax\n')
                out.write('    push rbx\n')
            elif operation[0] == OP_DUMP:
                out.write('    ; -- dump --\n')
                out.write('    pop rdi\n')
                out.write('    call dump\n')
            elif operation[0] == OP_EQUAL:
                out.write('    ; -- equal --\n')
                out.write('    mov rcx, 0\n')
                out.write('    mov rdx, 1\n')
                out.write('    pop rax\n')
                out.write('    pop rbx\n')
                out.write('    cmp rax, rbx\n')
                out.write('    cmove rcx, rdx\n')
                out.write('    push rcx\n')
            elif operation[0] == OP_IF:
                out.write('    ; -- if --\n')
                out.write('    pop rax\n')
                out.write('    test rax, rax\n')
                assert len(operation) >= 2, f'{Fore.RED}`if`{Style.RESET_ALL} instruction does not '+\
                f'have a reference to the end its block. Please call {Fore.YELLOW}cross_reference_blocks(){Style.RESET_ALL}'
                out.write('    jz addr_%d\n' % operation[1])
            elif operation[0] == OP_ELSE:
                out.write("    ;; -- else --\n")
                assert len(operation) >= 2, f'{Fore.RED}`else`{Style.RESET_ALL} instruction does not '+\
                f'have a reference to the end its block. Please call {Fore.YELLOW}cross_reference_blocks(){Style.RESET_ALL}'
                out.write("    jmp addr_{}\n".format(operation[1]))
                out.write('addr_{}:\n'.format((addr + 1)))
            elif operation[0] == OP_END:
                out.write('addr_%d:\n' % addr)
            else:
                assert False, 'unreachable'

        out.write('    mov rax, 60\n')
        out.write('    mov rdi, 0\n')
        out.write('    syscall\n')

# Checkout tokenization
def parser_token_as_operation(token):
    (file_path, row, column, word) = token
    assert COUNT_OPS == 8, 'Exhaustive operation handling in parser_token_as_operation'

    if word == '+':
        return plus()
    elif word == '-':
        return minus()
    elif word == '.':
        return dump()
    elif word == '=':
        return equal()
    elif word == 'if': # IF block code = 'if' + 'end'
        return if_block()
    elif word == 'end':
        return end_block_code()
    elif word == 'else':
        return else_op()
    else:
        try:
            return push(int(word))
        except ValueError as err:
            print(f'{Fore.YELLOW}[Reading]{Style.RESET_ALL} {file_path}\nreturned [{row}:{column}]' +
            f' -> {Fore.RED}{err}{Style.RESET_ALL} in Line: {row + 1} and Column: {column}')
            exit(1)

def cross_reference_blocks(program):
    stack = []

    for addr in range(len(program)):
        operation = program[addr]

        assert COUNT_OPS == 8, 'Exhaustive handling of operations in cross_reference_program. '+\
        'Keep in mind that not all of the operations need to be handled in here. Only those '+\
        'form blocks.'

        if operation[0] == OP_IF:
            stack.append(addr)

        elif operation[0] == OP_ELSE:
            if_addr = stack.pop()
            assert program[if_addr][0] == OP_IF, '`else` can only close if block'
            program[if_addr] = (OP_IF, addr + 1)
            stack.append(addr)

        elif operation[0] == OP_END:
            block_addr = stack.pop()
            if program[block_addr][0] == OP_IF or program[block_addr][0] == OP_ELSE:
                program[block_addr] = (program[block_addr][0], addr)
            else:
                assert program[block_addr][0] == OP_IF, '`end` can only close `if-else` block'

    return program

def find_column(line, start, predicate):
    while start < len(line) and not predicate(line[start]):
        start += 1
    return start

def lexer_line(line):
    column = find_column(line, 0, lambda x: not x.isspace())

    while column < len(line):
        column_end = find_column(line, column, lambda x: x.isspace())
        yield (column, line[column:column_end])
        column = find_column(line, column_end, lambda x: not x.isspace())

def lexer_file(file_parh):
    with open(file_parh, 'r') as file:
        return [
            (file_parh, row, col, token)
            for (row, line) in enumerate(file.readlines())
            for (col, token) in lexer_line(line)]

def load_program_from_file(file_path):
    return cross_reference_blocks(
        [parser_token_as_operation(token) for token in lexer_file(file_path)])

def usage_mode():
    """Usage: snake <SUBCOMMAND> <ARGS>
    SUBCOMMANDS:
    run       <file>  Simulate the program without compile

    compile   <file>  Compile the program and generate
                      a executable binary x86_64 Linux
    """

def call_subcommand(cmd, **kwargs):
    print(f'{Fore.YELLOW}[RUNING]{Style.RESET_ALL} ' + ' '.join(map(shlex.quote, cmd)))
    return subprocess.call(cmd, **kwargs)

def uncons(xs):
    return (xs[0], xs[1:])

if __name__ == '__main__':
    argv = sys.argv
    assert len(argv) >= 1
    (program_name, argv) = uncons(argv)

    if len(argv) < 1:
        print(usage_mode.__doc__)
        print('ERROR: it is necessary to supply a subcommand')
        exit(1)
    (subcommand, argv) = uncons(argv)

    if subcommand == 'run':
        if len(argv) < 1:
            usage_mode()
            print('ERROR: no input file is provided for the simulate')
            exit(1)

        (program_path, argv) = uncons(argv)
        program = load_program_from_file(program_path);
        simulate_program(program)

    elif subcommand == 'compile':
        if len(argv) < 1:
            print(usage_mode.__doc__)
            print('ERROR: no input file is provided for the compile')
            exit(1)

        (program_path, argv) = uncons(argv)
        program = load_program_from_file(program_path);
        basename = path.basename(program_path)

        DOT_SNAKE_EXTENSION = '.snake'
        if basename.endswith(DOT_SNAKE_EXTENSION):
            basename = basename[:-len(DOT_SNAKE_EXTENSION)]

        print(f'{Fore.GREEN}[INFO]{Style.RESET_ALL} Generating {program_path}')
        compile_program(program, basename + '.asm')
        call_subcommand(['nasm', '-felf64', basename + '.asm'])
        call_subcommand(['ld', '-o', basename, basename + '.o'])

    else:
        print(f'ERROR: unknown subcommand: \"{subcommand}\"\n')
        print(f'Try using this:\n{usage_mode.__doc__}')
        exit(1)
