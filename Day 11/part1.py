import time

def solve(filename):
    start_time = int(time.time() * 1000)

    arrangement = [int(i) for i in open(filename).read().split(' ')] #if i == to apply filtering
    # print(arrangement)

    blinks = 0

    final_arrangement = []
    while blinks < 25:
        
        iteration_arrangement = []
        for stone in arrangement:
            if stone == 0:
                # print('stone 0 creating stone 1')
                iteration_arrangement.append(1)
                continue

            # check if number of digits is even
            if len(str(stone)) % 2 == 0:
                # print('stone is even digits', stone, 'creating', int(str(stone)[:len(str(stone))//2]), int(str(stone)[len(str(stone))//2:]))
                # create two stones, first stone with the first half of the original stone digits, second stone the other half
                iteration_arrangement.append(int(str(stone)[:len(str(stone))//2]))
                iteration_arrangement.append(int(str(stone)[len(str(stone))//2:]))
                continue
            else:
                # print('stone is odd digits so * 2024', stone)
                iteration_arrangement.append(stone * 2024)
                continue

        arrangement = iteration_arrangement
        # print(blinks, iteration_arrangement)
        final_arrangement = iteration_arrangement
        blinks += 1        

    print(len(final_arrangement))
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

solve('test.txt')
solve('input.txt')