import time

def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    data = [i.split('\n') for i in raw_input.split('\n\n')]
        
    inputs = {}
    for row in data[0]:
        k, v = row.split(': ')
        inputs[k] = int(v)

    z_outputs = []
    operations = []
    for operation in data[1]:
        i1, gate, i2, _, output  = operation.split(' ')
        operations.append((i1, gate, i2, output))
        
        if output[0] == 'z':
            z_outputs.append(output)

    while not is_complete(inputs, z_outputs):
        run_operations(inputs, operations)

    # print(z_outputs)
    # print(inputs)
    output_result(inputs, z_outputs)

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def output_result(inputs, z_outputs):
    z_outputs.sort(reverse = True)

    binary_output = ''
    for z_output in z_outputs:
        binary_output += str(inputs[z_output])

    print(int(binary_output, 2))

def run_operations(inputs, operations):
    for operation in operations:
        execute(inputs, operation)

def execute(inputs, operation):
    i1, gate, i2, output = operation

    if i1 not in inputs or i2 not in inputs:
        return

    if gate == 'AND':
        inputs[output] = inputs[i1] & inputs[i2]
    elif gate == 'OR':
        inputs[output] = inputs[i1] | inputs[i2]
    elif gate == 'XOR':
        inputs[output] = inputs[i1] ^ inputs[i2]

def is_complete(inputs, z_outputs):
    for z_output in z_outputs:
        if z_output not in inputs:
            return False

    return True

solve('test.txt')
solve('test2.txt')
solve('input.txt')