import time
import graphviz

# full adder circuit with carry, not sure how to fully solve programatically
# instead, use graphviz to plot and visualize the graph and connections
# observations
# - full adder circuit with carry 
# - all the z outputs must follow the full adder pattern which looks like (excluding first and last output)
#  x  y
#   \/   CARRY 
#   AND   AND  x  y 
#      \  /    \ /
#       OR    XOR
#         \  /
#         XOR
#         |
#         Z
# - find all outputs where this does not match
# - we don't actually need to perform the swap
# - we just need to identify the 8 output wires the would need to be swapped

def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    data = [i.split('\n') for i in raw_input.split('\n\n')]
        
    inputs = reset_inputs(data)
    
    raw_operation_data = data[1]

    run(raw_operation_data, inputs)

    # not following full adder patterm
    all_wires_to_swap = ['cdj', 'z08', 'z16', 'mrb', 'z32', 'gfm', 'qjd', 'dhm']
    all_wires_to_swap.sort()
    print('all wires to swap', ','.join(all_wires_to_swap))

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def run(raw_operation_data, inputs):
    z_outputs = []
    operations = []    

    for operation in raw_operation_data:
        i1, gate, i2, _, output  = operation.split(' ')
        operations.append((i1, gate, i2, output))
        
        if output[0] == 'z':
            z_outputs.append(output)

    while not is_complete(inputs, z_outputs):
        run_operations(inputs, operations)

    # print(z_outputs)
    # print(inputs)    
    incorrect_z = check_result(inputs, z_outputs)

    generate_graph(inputs, operations, incorrect_z)

    if incorrect_z == []:
        print('circuit is working')
        return True
    
    return False

def generate_graph(inputs, operations, incorrect_z):
    graph = graphviz.Digraph()

    for i1, gate, i2, output in operations:
        graph.node(i1, i1 + ' ' + str(inputs[i1]))
        graph.node(i2, i2 + ' ' + str(inputs[i2]))

        if output[0] == 'z':
            if output in incorrect_z:
                graph.node(output, output + ' ' + str(inputs[output]), style='filled', fillcolor='red')
            else:
                graph.node(output, output + ' ' + str(inputs[output]), style='filled', fillcolor='lightgreen')
        else:
            graph.node(output, output)

        gate_node = ' '.join([i1,gate,i2])
        graph.node(gate_node, gate_node)
        
        graph.edge(i1, gate_node)
        graph.edge(i2, gate_node)
        graph.edge(gate_node, output)

    graph.render('graph', view=True)

def check_result(inputs, z_outputs):
    x_inputs = []
    y_inputs = []
    for input in inputs.keys():
        if input[0] == 'x':
            x_inputs.append(input)
        if input[0] == 'y':
            y_inputs.append(input)

    x_inputs.sort(reverse = True)
    y_inputs.sort(reverse = True)
    z_outputs.sort(reverse = True)

    x_binary = get_binary(inputs, x_inputs)
    y_binary = get_binary(inputs, y_inputs)
    z_binary = get_binary(inputs, z_outputs)

    print('x    ', x_binary, int(x_binary, 2))
    print('y    ', y_binary, int(y_binary, 2))
    x_y_int = int(x_binary, 2) + int(y_binary, 2)
    x_y_binary = format(x_y_int, 'b')
    print('x + y', x_y_binary, x_y_int)
    print('z    ', z_binary, int(z_binary, 2))

    return get_incorrect(z_binary, x_y_binary)

def get_incorrect(actual, expected):
    incorrect_z = []
    for i in range(1, len(actual)+1):
        if actual[-i] != expected[-i]:
            incorrect_z.append('z' + str(i-1).rjust(2, '0'))

    print('incorrect z', incorrect_z)
    return incorrect_z

def get_binary(inputs, nodes):
    binary_output = ''
    for node in nodes:
        binary_output += str(inputs[node])
    return binary_output

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

def reset_inputs(data):
    inputs = {}
    for row in data[0]:
        k, v = row.split(': ')
        inputs[k] = int(v)
    return inputs

solve('input.txt')