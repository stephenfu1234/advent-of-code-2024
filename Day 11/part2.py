import time
import functools

# use caching as there will be a lot of repeating the same transformation on each blink
def solve(filename):
    start_time = int(time.time() * 1000)

    arrangement = [int(i) for i in open(filename).read().split(' ')] #if i == to apply filtering
    # print(arrangement)
    
    total_stones = 0
    for initial_stone in arrangement:
        max_blinks = 75
        
        # wrap as a tuple so that it can be cached as a list is unhashable with functools
        stones_created = apply_blinks(tuple([initial_stone]), max_blinks)
        # print('initial stone', initial_stone, 'created', stones_created, 'stones')

        total_stones += stones_created
    print(total_stones)

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

@functools.cache
def apply_blinks(stones, blinks_remaining):
    total_stones = 0

    # we don't care about the actual value returned, only the total number of stones created
    if blinks_remaining == 0:
        return len(stones)
    
    # for each stone, recursively apply the blink transformation until no more blinks remaining
    # at the final blink we will return how many stones were created for the previous stone
    # we can then sum them up to return the total number of stones created for the original starting stone
    # the functools.cache helps to avoid duplication of effort which is important when increasing
    # the number of blinks as the amount of repeated numbers like 0 and 1 will greatly increase
    for stone in stones:
        total_stones += apply_blinks(tuple(transform_stone(stone)), blinks_remaining - 1)

    return total_stones

def transform_stone(stone):
    if stone == 0:
        return [1]
               
    if len(str(stone)) % 2 == 0:
        return [int(str(stone)[:len(str(stone))//2]),int(str(stone)[len(str(stone))//2:])]
    
    return [stone * 2024]

solve('test.txt')
solve('input.txt')