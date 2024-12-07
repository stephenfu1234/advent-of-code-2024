import time

def solve(filename):
    start_time = int(time.time() * 1000)

    valid_equations = []
    
    for line in open(filename).read().splitlines():
        test_value, numbers = line.split(': ')
        # print(line)
        
        remaining_numbers = list(map(int,numbers.split(' ')))
        current_value = remaining_numbers.pop(0)

        if bfs_test(int(test_value), remaining_numbers, '+', current_value, str(current_value)):
            valid_equations.append(int(test_value))
        elif bfs_test(int(test_value), remaining_numbers, '*', current_value, str(current_value)):
            valid_equations.append(int(test_value))
        elif bfs_test(int(test_value), remaining_numbers, '||', current_value, str(current_value)):
            valid_equations.append(int(test_value))

    # print(valid_equations)
    print(sum(valid_equations))
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

# breadth first search test of the binary tree
def bfs_test(test_value, numbers, operator, current_value, equation):
    remaining_numbers = numbers.copy()

    next_number = remaining_numbers.pop(0)
    equation = equation + operator + str(next_number)

    # print('testing', current_value, operator, next_number, 'and remaining numbers', remaining_numbers)

    # apply text evaluation as the operator is a string representation of + or *
    if operator == '||':
        current_value = int(str(current_value) + str(next_number))
    else:
        current_value = eval(str(current_value) + operator + str(next_number))

    # end the search if this branch has already exceeded the target
    if current_value > test_value:
        return False
        
    # if there are no more numbers to process then check if test_value is met 
    if remaining_numbers == []:
        # if current_value == test_value:
        #     print('success', equation)
        return current_value == test_value
    
    # continue the test with the remaining numbers for both operators
    add_test = bfs_test(test_value, remaining_numbers, '+', current_value, equation)
    if add_test:
        return True
    
    mul_test = bfs_test(test_value, remaining_numbers, '*', current_value, equation)
    if mul_test:
        return True
    
    concat_test = bfs_test(test_value, remaining_numbers, '||', current_value, equation)
    if concat_test:
        return True

solve('test.txt')
solve('input.txt')