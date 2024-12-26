import time
import functools

# initially tried a recursive depth first search but this was too slow because you have to explore the entire search space to determine no solution
# the approach attempted to use a towel against any part of the design and split the design into separate sections then recursively run on each section
# instead its simplified to still use a recursive approach but just chop off the start of the design, this massively reduces the search space
def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    data = [i for i in raw_input.split('\n\n')]    
    towels = data[0].split(', ')
    designs = data[1].split('\n')

    # print(towels)
    # print(designs)

    total_possible_designs = 0
    for design in designs:
        print('testing', design)
        total_possible_designs += possible_combinations(tuple(towels), design, 0)
            

    print('total possible designs', total_possible_designs)

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')


@functools.cache
def possible_combinations(towels, design, idx):
    # print('design', design, 'idx', idx)
    if idx == len(design):
        return 1

    count = 0
    for towel in towels:
        # for each towel, try using it against the start of the design
        # print(towel, design[idx:idx + len(towel)])
        if towel == design[idx:idx + len(towel)]:
            # if the towel can be used, the remove it from the design and recursively continue
            # print(towel, 'towel can be used, continue with the rest of the design')
            count += possible_combinations(tuple(towels), design, idx + len(towel))

    return count

solve('test.txt')
solve('input.txt')