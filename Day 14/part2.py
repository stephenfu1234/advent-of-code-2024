import time
import itertools 

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

    # simulate many iterations
    # for each iteration, see if we have a cluster of robots next to each other
    # then print that as a potential solution
    seconds = 20000
    required_cluster_size = 8
    for i in range(seconds):
        drawing = [[' ' for _ in range(max_x)] for _ in range(max_y)]
        final_positions = []

        for robot in robots:
            x, y = robot[0]
            vx, vy = robot[1]

            new_x = (x + (vx * i)) % max_x
            new_y = (y + (vy * i)) % max_y

            drawing[new_y][new_x] = 'X'
            final_positions.append((new_x, new_y))

        sorted_by_y = dict()
 
        # group the robot locations by their y position
        # then for each row we can see how many robots are lined up next to each other
        for row, robot in itertools.groupby(sorted(final_positions, key=lambda ele: ele[1]), key=lambda ele: ele[1]):
            sorted_by_y[row] = [ele[0] for ele in robot]

        widest_horizontal_line = 0
        for y_location, x_locations in sorted_by_y.items():
            # new to convert to set as multiple robots in same location will affect the consecutive ordering e.g 1,2,2,3 instead of 1,2,3
            consecutive_groups = find_consecutive_numbers(sorted(set(x_locations)))
            # print(y_location, sorted(set(x_locations)), consecutive_groups)
            for group in consecutive_groups:
                if len(group) > widest_horizontal_line:                    
                    widest_horizontal_line = len(group)
            
        # if we have robots lined up horizontally then output and see if it looks like a valid solution
        if widest_horizontal_line >= required_cluster_size:
            for line in drawing:
                print(''.join(line))
            
            print('Found cluster of', required_cluster_size, 'robots after', i, 'seconds')            
            break           

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def find_consecutive_numbers(numbers): 
    consecutive_groups = [] 
    current_group = [] 
 
    for i in range(len(numbers)): 
        if i == 0 or numbers[i] == numbers[i - 1] + 1: 
            current_group.append(numbers[i]) 
        else: 
            if len(current_group) > 1: 
                consecutive_groups.append(current_group) 
            current_group = [numbers[i]] 
     
    # Check if the last group is consecutive 
    if len(current_group) > 1: 
        consecutive_groups.append(current_group)
 
    return consecutive_groups 

# solve('test.txt', 11, 7)
solve('input.txt', 101, 103)