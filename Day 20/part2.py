import time
import copy

def solve(filename, required_time_saving):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    # read into a list of lists, split by new line and then by space using list comprension
    maze = [list(i) for i in raw_input.split('\n')]

    start_location = None
    end_location = None
    for row_idx, row in enumerate(maze):
        for col_idx, col in enumerate(row):
            if col == 'S': start_location = (row_idx, col_idx)
            if col == 'E': end_location = (row_idx, col_idx)

    visited = find_shortest_path(maze, start_location, end_location)

    time_savings = find_shortcuts(maze, visited)

    required_savings = []
    savings_frequency = {i:time_savings.count(i) for i in set(time_savings)}
    for key, value in savings_frequency.items():
        # print(value, 'cheats that save', key, 'picoseconds')
        if key >= required_time_saving:
            required_savings.append(value)
            
    print(sum(required_savings), 'cheats with at least', required_time_saving, 'picoseconds')
    
    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')

def find_shortest_path(maze, start, end):
    draw_individual_moves = False
    directions = [(-1,0),(0,1),(0,-1),(1,0)]
    to_visit = [(start[0], start[1], [], 0)]
    seen = {}
    iterations = 1
    
    while to_visit != []:
        iterations += 1
        # r, c, visited, cost = to_visit.pop() # LIFO for deep first search
        r, c, visited, cost = to_visit.pop(0) # FIFO for breadth first search
        
        if draw_individual_moves:
            input("Press the enter for next move") 
            draw_maze(maze, visited)

        # if we've been here before and it was cheaper then stop
        if (r, c) in seen and seen[(r,c)] <= cost:
            continue
        else:
            # track where we have currently visited and what the current cost to reach here is
            new_visited = copy.deepcopy(visited)
            new_visited.append((r, c, cost))
            seen[(r, c)] = cost

            if (r, c) == end:
                print('found end location with cost', cost)
                print('route taken')
                draw_maze(maze, new_visited)
                return new_visited
                # print('finished with lowest cost', seen[end], 'after', iterations, 'iterations')
                # return # for immediate stop

            for dr, dc in directions:
                if maze[r+dr][c+dc] == '#':
                    continue
            
                # now add it to the stack of places to next visit and increment the step cost
                to_visit.append((r+dr, c+dc, new_visited, cost+1))
    
def find_shortcuts(maze, visited):
    # print(visited)
    
    # to find a shortcut look at all the visited locations
    # find all locations where they are separated by 1 or 2 (vertitical and horizonal)
    # don't compare to a location that is within 2 prior steps
    visited_pairs = [(a, b) for idx, a in enumerate(visited) for b in visited[idx + 1:]]
    # print(len(visited_pairs))

    # remove pairs where cost < 2
    filtered_pairs = list(filter(lambda visited_location: abs(visited_location[0][2]-visited_location[1][2]) >= 20, visited_pairs))
    # print(len(filtered_pairs))

    # remove pairs where the distance is > 2 squares e.g. (2, 3) and (1,2) = 1 + 1 = 2 squares distance
    # this will give us all the locations where we can apply a shortcut    
    filtered_pairs = list(filter(lambda visited_location: abs(visited_location[0][0]-visited_location[1][0]) + \
                                                          abs(visited_location[0][1]-visited_location[1][1]) <= 20, filtered_pairs))
    # print(len(filtered_pairs))
    
    time_savings = []
    for pair in filtered_pairs:
        distance = abs(pair[0][0]-pair[1][0]) + abs(pair[0][1]-pair[1][1])
        saving = abs(pair[0][2] - pair[1][2]) - distance
        # print(pair, 'saves', saving, 'picoseconds')
        time_savings.append(saving)

        if saving == 80:
            print(pair)

    return time_savings

def draw_maze(maze, steps_taken):
    completed_maze = copy.deepcopy(maze)

    if steps_taken != None:
        for r, c, _ in steps_taken:
            completed_maze[r][c] = 'O'

    for line in completed_maze:
        print(''.join(line))

# solve('test.txt', 50)
solve('input.txt', 100)