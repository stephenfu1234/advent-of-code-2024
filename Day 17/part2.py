import time

# after setting register A to 0 and printing what output we can see a pattern
# 3 bit pattern (as the pattern changes for every increase of 8 which (000 to 111 in binary)
# each time the we output, it outputs on modulo 8 (lowest 3 bits) and then sets register A to this 3 bit value
# so to continue with finding the rest of the output we can left bit shift by 3 and repeat the process, this time matching the last 2 output digits and so on
def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    data = [[j.split(': ') for j in i.split('\n')] for i in raw_input.split('\n\n')] #if i == to apply filtering
    registers_raw = data[0]

    registers = set_registers(int(registers_raw[0][1]), int(registers_raw[1][1]), int(registers_raw[2][1]))
    
    program_raw = list(eval(data[1][0][1]))
    # group a list of [1,2,3,4,5,6] into [(1,2), (3,4), (5,6)]
    program = list(zip(program_raw[::2], program_raw[1::2]))

    print(program)
   
    register_A = 1
    output_part_to_match = 1
    while True:
        registers = set_registers(register_A, int(registers_raw[1][1]), int(registers_raw[2][1]))
        output = run_program(program, registers)

        print('initial register A', register_A)
        print('current output', output)
        print('target output',data[1][0][1].split(','))

        if output == data[1][0][1].split(','):
            print('setting initial register A', register_A, 'will match the target program')
            break

        if output[-output_part_to_match:] != list(map(str,program_raw))[-output_part_to_match:]:
            register_A += 1
        else:
            print('last', output_part_to_match, 'output digits are matching', output[-output_part_to_match])
            # input("Press the enter for next move") 
            register_A = register_A << 3
            output_part_to_match += 1

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')


def set_registers(a, b, c):
    registers = {}
    registers['A'] = a
    registers['B'] = b
    registers['C'] = c

    return registers

def run_program(program, registers):
    output = []
    pointer = 0
    while pointer < len(program):        
        opcode, combo_operand = program[pointer]
        operand = get_operand_value(registers, combo_operand)
        # print('opcode', opcode, 'with combo operand', combo_operand, 'returns', operand)
        
        if opcode == 0:
            registers['A'] = registers['A'] // 2**operand
        elif opcode == 1:
            registers['B'] = registers['B'] ^ combo_operand
        elif opcode == 2:
            registers['B'] = operand % 8
        elif opcode == 3:
            if registers['A'] != 0:
                pointer = operand
                continue
        elif opcode == 4:
            registers['B'] = registers['B'] ^ registers['C']
        elif opcode == 5:
            output.append(str(operand % 8))
        elif opcode == 6:
            registers['B'] = registers['A'] // 2**operand
        elif opcode == 7:
            registers['C'] = registers['A'] // 2**operand

        pointer += 1
    
    return output

def get_operand_value(registers, operand):
    if operand >= 0 and operand <= 3:
        return operand
    
    if operand == 4:
        return registers['A']
    
    if operand == 5:
        return registers['B']
    
    if operand == 6:
        return registers['C']

solve('test7.txt')
print()
solve('input.txt')