import time
import re

def solve(filename):
    start_time = int(time.time() * 1000)

    total = 0
    pattern = r'mul[(]\d{1,3},\d{1,3}[)]'

    # remove the new lines as the new line means we don't find the previous don't
    for do in ''.join(open(filename).read().splitlines()).split('do()'):
        # split by do and then by don't.  After splitting by don't we know everything after the first element should be ignored
        operations = re.findall(pattern, do.split('don\'t()')[0])
        for operation in operations:
            # mul(2,4), remove first 4 and last char and then split by comma
            # then use list(map(int, my_str_list)) to convert list of str to ints
            l, r = (list(map(int, operation[4:][:-1].split(','))))
            total += l * r

    print(total)
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

solve('test2.txt')
solve('input.txt')