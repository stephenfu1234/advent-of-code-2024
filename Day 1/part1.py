import time

def read_file(filename):
    return open(filename).read()

def solve(filename):
    start_time = int(time.time() * 1000)

    # for line in read_file(filename).splitlines():
    #     dir, dist = line.split()
    raw_input = read_file(filename)

    # read into a list of lists, split by new line and then by space using list comprension
    data = [i.split('   ') for i in raw_input.split('\n')] #if i == to apply filtering

    left = []
    right = []

    for l, r in data:
        left.append(int(l))
        right.append(int(r))

    left.sort()
    right.sort()

    result = [abs(l - r) for l, r in zip(left, right)]

    print(sum(result))
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

solve('test.txt')
solve('input.txt')