import time

def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    schematics = [i.split('\n') for i in raw_input.split('\n\n')]
    
    locks = set()
    keys = set()

    for schematic in schematics:
        if schematic[0][0] == '#':
            locks.add(tuple(get_heights(schematic)))
        else:
            keys.add(tuple(get_heights(schematic)))
    
    # print(locks)
    # print(keys)
    
    total_matching = find_matching(locks, keys)
    print(total_matching)

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def find_matching(locks, keys):
    total_matching = 0
    for lock in locks:
        for key in keys:
            # print('lock', lock, 'key', key)
            if is_fit(lock, key):
                # print('fits')
                total_matching += 1
    return total_matching

def is_fit(lock, key):
    combined_heights = [sum(x) for x in zip(lock, key)]
    for combined_height in combined_heights:
        if combined_height >= 6:
            return False
        
    return True
    
def get_heights(schematic):
    heights = []
    for c in range(len(schematic[0])):
        heights.append([row[c] for row in schematic].count('#')-1)
    return heights

solve('test.txt')
solve('input.txt')