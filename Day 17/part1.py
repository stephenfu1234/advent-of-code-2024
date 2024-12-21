import time

def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    # read into a list of lists, split by new line and then by space using list comprension
    data = [[j.split(': ') for j in i.split('\n')] for i in raw_input.split('\n\n')] #if i == to apply filtering
    registers_raw = data[0]

    registers = {}
    registers['A'] = int(registers_raw[0][1])
    registers['B'] = int(registers_raw[1][1])
    registers['C'] = int(registers_raw[2][1])
    
    program_raw = list(eval(data[1][0][1]))
    # group a list of [1,2,3,4,5,6] into [(1,2), (3,4), (5,6)]
    program = list(zip(program_raw[::2], program_raw[1::2]))

    print(program)

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

    print('program output',','.join(output))
    print('registers', registers)
       
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def get_operand_value(registers, operand):
    if operand >= 0 and operand <= 3:
        return operand
    
    if operand == 4:
        return registers['A']
    
    if operand == 5:
        return registers['B']
    
    if operand == 6:
        return registers['C']

solve('test.txt')
print()
solve('test2.txt')
print()
solve('test3.txt')
print()
solve('test4.txt')
print()
solve('test5.txt')
print()
solve('test6.txt')
print()
solve('input.txt')