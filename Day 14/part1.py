import time

def solve(filename, max_x, max_y):
    start_time = int(time.time() * 1000)

    # for line in open(filename).read().splitlines():
    #     dir, dist = line.split()
    raw_input = open(filename).read()
    
    cleaned_input = raw_input.replace('p=', '')
    cleaned_input = cleaned_input.replace('v=', '')

    # read into a list of lists, split by new line and then by space using list comprension
    robots = [[eval(j) for j in i.split(' ')] for i in cleaned_input.split('\n')] #if i == to apply filtering

    # print(robots)
    
    # determine quandrant boundaries (min_x, max_x, min_y, max_y)
    quadrant_1 = (0, (max_x//2 - 1), 0, (max_y//2 - 1))
    quadrant_2 = ((max_x//2 + 1), max_x - 1, 0, (max_y//2 - 1))
    quadrant_3 = (0, (max_x//2 - 1), (max_y//2 + 1), max_y - 1)
    quadrant_4 = ((max_x//2 + 1), max_x - 1, (max_y//2 + 1), max_y - 1)
    
    # print(quadrant_1)
    # print(quadrant_2)
    # print(quadrant_3)
    # print(quadrant_4)

    quadrant_1_robots = quadrant_2_robots = quadrant_3_robots = quadrant_4_robots = 0
        
    seconds = 100    
    for robot in robots:
        x, y = robot[0]
        vx, vy = robot[1]

        new_x = (x + (vx * seconds)) % max_x
        new_y = (y + (vy * seconds)) % max_y

        # print(x, y, 'at vector', vx, vy, 'arrives at', new_x, new_y, 'after', seconds, 'seconds')

        if quadrant_1[0] <= new_x and new_x <= quadrant_1[1] and quadrant_1[2] <= new_y and new_y <= quadrant_1[3]:
            quadrant_1_robots += 1
            continue
        
        if quadrant_2[0] <= new_x and new_x <= quadrant_2[1] and quadrant_2[2] <= new_y and new_y <= quadrant_2[3]:
            quadrant_2_robots += 1
            continue

        if quadrant_3[0] <= new_x and new_x <= quadrant_3[1] and quadrant_3[2] <= new_y and new_y <= quadrant_3[3]:
            quadrant_3_robots += 1
            continue

        if quadrant_4[0] <= new_x and new_x <= quadrant_4[1] and quadrant_4[2] <= new_y and new_y <= quadrant_4[3]:
            quadrant_4_robots += 1
            continue
        
    # print(quadrant_1_robots)
    # print(quadrant_2_robots)
    # print(quadrant_3_robots)
    # print(quadrant_4_robots)
    print(quadrant_1_robots * quadrant_2_robots * quadrant_3_robots * quadrant_4_robots)

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

solve('test.txt', 11, 7)
solve('input.txt', 101, 103)