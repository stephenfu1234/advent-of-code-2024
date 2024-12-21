import time

def solve(filename):
    start_time = int(time.time() * 1000)

    raw_input = open(filename).read()

    # read into a list of lists, split by new line and then by space using list comprension
    maze = [list(i) for i in raw_input.split('\n')] #if i == to apply filtering

    # for line in maze:
    #     print(''.join(line))

    start_location = None
    end_location = None
    for row_idx, row in enumerate(maze):
        for col_idx, col in enumerate(row):
            if col == 'S':
                start_location = (row_idx, col_idx)
            if col == 'E':
                end_location = (row_idx, col_idx)

    directions = [(-1,0),(0,1),(0,-1),(1,0)]

    # store where to visit, the direction, the current cost and history e.g (1,1), (dr. dc), 0, []
    start_cost = 1001
    to_visit = [(start_location, (None, None), start_cost, [])]
    seen = {}
    steps = 0
     
    while to_visit != []:
        steps += 1
        # if steps == 10000:
        #     print('break steps')
        #     break
        # print('remaining steps', len(to_visit), [i[0] for i in to_visit])
        # print('\nremaining steps', len(to_visit))

        # pop(0) is FIFO - take first location for a breadth first search to evaluate options - this will be more optimal as it quickly rules out slow paths
        # pop() is LIFO - take last location for a depth first search which is greedy and tries to find the goal fist
        location, current_direction, current_cost, history = to_visit.pop(0)

        # keep track of where we have been and in which direction to avoid infinite loops
        seen[location] = current_cost
        new_history = history + [location]
        r, c = location

        # add step cost excluding the start location
        if current_direction != (None, None):
            current_cost += 1

        # print('at', location, 'travelling', current_direction, 'with current cost', current_cost)

        # if at end location, continue in case we find other optimal paths
        if location == end_location:
            # print('found end location', location, 'travelling', current_direction, 'with current cost', current_cost, 'with path', new_history)
            continue

        # goto available directions
        for new_direction in directions:
            dr, dc = new_direction
            new_location = (r+dr,c+dc)

            # don't go backwards i.e. if travelling (0,1), dont go backwards (0,-1)
            if current_direction == tuple(i * -1 for i in new_direction):            
                continue

            if new_location in seen:
                # this direction we have already visited
                # if the cost to this prior location is cheaper then skip
                # print(new_location, location)
                if new_location in seen and seen[new_location] < current_cost:
                    # print('moving from', location, 'with direction', new_direction, 'to', new_location, 'takes us to previously seen location which had cheaper cost', seen[new_location], ', our current cost is', current_cost)
                    continue

            if maze[r+dr][c+dc] == '.' or maze[r+dr][c+dc] == 'E':
                # if we have to change direction then add rotate cost
                new_cost = current_cost
                if current_direction != (None, None) and current_direction != new_direction:
                    new_cost += 1000
                    # print('which requires a turn, cost increased from', current_cost, 'to', new_cost)

                
                # print('adding new location to visit', new_location, 'with direction', new_direction, 'with cost', new_cost)
                to_visit.append((new_location, new_direction, new_cost, new_history))

        # print('new remaining steps', to_visit)
        # print('new remaining steps', len(to_visit), [i[0] for i in to_visit])
    print('steps required', steps)
    print('lowest cost', seen[end_location])

    end_time = int(time.time() * 1000)
    print(f'Time taken for {filename} (ms): {end_time - start_time}')



solve('test.txt')
print()
solve('test2.txt')
print()
solve('input.txt')